#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# ============ #
# PEPPER_ROBOT #
# ============ #
# Model class for the Pepper Robot
#
# @author ES
# **

import functools
import logging
import time
from PyQt5.QtCore import pyqtSignal, QThread

import es_common.hre_config as pconfig  # TODO: replace!
from es_common.enums.led_enums import LedColor
from es_common.enums.robot_name import RobotName
from robot_manager.pepper.enums.engagement_enums import EngagementMode, EngagementZone
from robot_manager.pepper.enums.motion_enums import Animation, AutonomousLife
from robot_manager.pepper.enums.sensor_enums import Sonar, LedName
from robot_manager.pepper.enums.tablet_enums import TabletAction
from robot_manager.pepper.handler.animation_handler import AnimationHandler
from robot_manager.pepper.handler.connection_handler import ConnectionHandler
from robot_manager.pepper.handler.engagement_handler import EngagementHandler
from robot_manager.pepper.handler.screen_handler import ScreenHandler
from robot_manager.pepper.handler.sensor_handler import SensorHandler
from robot_manager.pepper.handler.speech_handler import SpeechHandler
from robot_manager.pepper.model.person import Person
from thread_manager.db_threads import DBChangeStreamThread


class PepperRobot(QThread):
    update_people_signal = pyqtSignal(bool)

    def __init__(self, name=RobotName.PEPPER):
        super(PepperRobot, self).__init__()
        self.logger = logging.getLogger("SoftBank Robot")

        self.name = name
        self.touch = None
        self.is_interacting = False
        self.is_in_engagement_mode = False
        self.pid = 0  # person id
        self.last_input = None
        self.person_approached, self.person_approached_event = (None,) * 2
        self.is_engaged_signal, self.block_completed_signal, self.user_answer_signal = (None,) * 3

        self.animation_handler, self.sensor_handler, self.engagement_handler = (None,) * 3
        self.speech_handler, self.screen_handler = (None,) * 2
        self.time_of_last_picture = 0
        self.people_in_zone_1 = None

        self.sound_detected = None
        self.session = None
        self.db_thread = DBChangeStreamThread()

    def connect(self, robot_ip, port):
        message, error, is_awake = [None, None, False]
        self.session = ConnectionHandler.create_qi_session(robot_ip, port)

        if self.session is None:
            return message, "\n*** Unable to connect to Naoqi:\n- IP: {} | Port: {}\n\n".format(robot_ip, port), is_awake

        try:
            self._init_handlers()

            message = "Successfully connected to Pepper:\n- IP: {} | Port: {}".format(robot_ip, port)
            is_awake = self.is_awake()
        except RuntimeError as e:
            error = "\n\n*** Unable to connect to Naoqi:\n- IP: {} | Port: {}\n{}".format(robot_ip, port, e)
        finally:
            return message, error, is_awake

    def _init_handlers(self):
        self.animation_handler = AnimationHandler(session=self.session)
        self.speech_handler = SpeechHandler(session=self.session)
        if self.name is None or self.name is RobotName.PEPPER:
            self.screen_handler = ScreenHandler(session=self.session)
        self.sensor_handler = SensorHandler(session=self.session)
        self.engagement_handler = EngagementHandler(session=self.session)

        self.logger.debug("\n\n\nInitiated the robot handlers.\n\n\n")

    """
    TOUCH EVENTS
    """

    def subscribe_to_touch_events(self):
        if self.touch is None:
            self.touch = self.sensor_handler.memory.subscriber("TouchChanged")

    def react_to_touch(self, message, led_name, led_color_start, led_color_end):
        self.sensor_handler.set_leds(led_name=led_name, led_color=LedColor.RED)
        self.complain(message=message)
        self.sensor_handler.set_leds(led_name=led_name, led_color=LedColor.WHITE)

    """
    SPEECH EVENTS
    """

    def subscribe_to_speech_events(self):
        self.speech_handler.speech_recognition.subscribe(pconfig.speech_recognition_user)
        self.last_input = self.speech_handler.memory.subscriber("Dialog/LastInput")

    def unsubscribe_to_speech_events(self):
        self.speech_handler.speech_recognition.unsubscribe(pconfig.speech_recognition_user)

    """
    DIALOG EVENTS
    """

    def subscribe_to_dialog_events(self, block_completed_signal, user_answer_signal):
        self.block_completed_signal = block_completed_signal
        self.user_answer_signal = user_answer_signal

        # Add the signals to DBThread and start listening
        self.db_thread.signals_dict['blockCompleted'] = self.block_completed_signal
        self.db_thread.signals_dict['userAnswer'] = self.user_answer_signal
        self.db_thread.start_listening()

    def raise_block_completed_event(self, val):
        if self.block_completed_signal is not None:
            self.block_completed_signal.emit(True)

    def raise_user_answer_event(self, val):
        if self.user_answer_signal is not None:
            self.user_answer_signal.emit(val)

    """
    SOUND EVENTS
    """

    def subscribe_to_sound_detection(self, sensitivity=pconfig.sound_sensitivity):
        self.sound_sensitivity(sensitivity=sensitivity)
        self.sound_detected = self.speech_handler.memory.subscriber("SoundDetected")
        self.sound_detected.signal.connect(functools.partial(self.on_sound_detected))

    def on_sound_detected(self, event_name, value):
        print("Sound detected:")
        print(value)

    def sound_sensitivity(self, sensitivity=pconfig.sound_sensitivity):
        self.speech_handler.sound_detector.setParameter("Sensitivity", sensitivity)

    """
    LED EVENTS
    """

    def set_leds(self, led_name=LedName.FACE, led_color=LedColor.WHITE, duration=0.5):
        self.sensor_handler.set_leds(led_name=led_name, led_color=led_color, duration=duration)

    """
    ENGAGEMENT EVENTS
    """

    def engagement(self, is_engaged_signal, start=True):
        try:
            if start:
                self.is_engaged_signal = is_engaged_signal
                self.subscribe_to_engagement_events(subscribe=True)
                self.is_in_engagement_mode = True
                self.logger.info("Engagement is set.")
                # self.move_and_animate(message = "Hello, how are you?")
            else:
                self.is_in_engagement_mode = False
                self.subscribe_to_engagement_events(subscribe=False)
                self.engagement_handler.set_engagement(mode=EngagementMode.UNENGAGED)
                self.posture(reset=True)
                # self.stop_dialog()
        except Exception as e:
            self.logger.error("Error while setting engagement: {}".format(e))

    def subscribe_to_engagement_events(self, subscribe=True):
        if subscribe is True:
            self.engagement_handler.subscribe()

            self.update_people_signal.connect(self.update_people)
            self.db_thread.signals_dict['updatePeople'] = self.update_people_signal
            self.db_thread.start_listening()
            self.logger.info("Successfully subscribed to engagement zones.")
        else:
            self.engagement_handler.unsubscribe()

    def update_people(self, event_name=None, value=None):
        if self.is_in_engagement_mode is True:  # otherwise, do nothing!
            self.people_in_zone_1 = self.engagement_handler.get_people(zone=EngagementZone.ZONE1)
            print("\n\nPeople in zone_1: {}\n\n".format(self.people_in_zone_1))
            if len(self.people_in_zone_1) > 0:
                self.logger.info("*** People in zone 1: {}".format(self.people_in_zone_1))

                if self.is_interacting is False:
                    self.pid = self.people_in_zone_1[0]
                    self.engage()

                # Stop the interaction if the person is not in zone 1 anymore
                if (self.is_interacting is True) and (self.pid not in self.people_in_zone_1):
                    self.update_engaged_person()

    def update_engaged_person(self):
        # search for the engaged person (30s) or update its id
        for _ in range(10):
            self.people_in_zone_1 = self.engagement_handler.get_people(zone=EngagementZone.ZONE1)
            if self.pid in self.people_in_zone_1:
                return True
            time.sleep(0.3)
        if len(self.people_in_zone_1) > 0:
            self.pid = self.people_in_zone_1[0]
            self.engage()

    def engage(self):
        self.engagement_handler.set_engagement(EngagementMode.FULLY_ENGAGED)
        self.engagement_handler.engage(self.pid)
        if self.is_interacting is False:
            self.is_engaged_signal.emit(True)
            self.logger.info("Pepper is ready to engage.")
        else:
            self.logger.info("Re-engaging...")

    def tracking(self, enable=True):
        self.engagement_handler.tracking(enable=enable)

    def face_tracker(self, start=True, face_width=pconfig.default_face_width):
        self.engagement_handler.face_tracker(start=start, face_width=face_width)

    def divert_look(self, gaze_pattern=None, thresh=pconfig.divert_look_threshold):
        self.engagement_handler.divert_look(gaze_pattern=gaze_pattern, thresh=thresh)

    """
    Animation control methods
    """

    def posture(self, wakeup=False, reset=False):
        if reset is True:
            self.animation_handler.reset_posture()
        else:
            self.animation_handler.wakeup() if wakeup == True else self.animation_handler.rest()

    def is_awake(self):
        return self.animation_handler.is_awake()

    def is_aware(self):
        return self.animation_handler.is_aware()

    def breathing(self, enable=False):
        self.animation_handler.set_breathing(enable)

    def head(self, reset=False):
        if reset is True:
            self.animation_handler.reset_head_pose()

    def autonomous_life(self, state=AutonomousLife.DISABLED):
        self.animation_handler.set_autonomous_life(state=state)

    def awareness(self, enable=False):
        self.animation_handler.set_awareness(enable=enable)
        if enable is False:
            self.posture(reset=True)

    def animate(self, animation=Animation.WAVE):
        self.animation_handler.animate(animation_name=animation)

    def execute_animation(self, animation_name):
        self.animation_handler.execute_animation(animation_name=animation_name)

    def led_animation(self, duration=1.0):
        self.sensor_handler.led_animation(duration=duration)

    def move_to(self, x=0, y=0, theta=0):
        self.animation_handler.move_to(x=x, y=y, theta=theta)

    def move_and_animate(self, x=0, y=0, theta=0, message=None, animation=Animation.WAVE):
        self.move_to(x, y, theta)
        self.animate(animation=animation) if message is None else self.animated_say(message=message,
                                                                                    animation_name=animation)

        # wait until move is finished, then move back to the previous position
        self.animation_handler.finish_move()
        self.move_to(-x, -y, -theta)

    # SPEECH:
    # -------
    def volume(self, level=0.5):
        self.speech_handler.set_volume(level=level)

    def language(self, name='English'):
        self.speech_handler.set_language(name=name)

    def say(self, message="Hi"):
        self.speech_handler.say(message=message)

    def animated_say(self, message=None, animation_name=None, robot_voice=None):
        self.speech_handler.animated_say(message=message, animation_name=animation_name, robot_voice=robot_voice)

    def complain(self, message="Hey"):
        self.animated_say(message=message)
        self.posture(reset=True)

    def customized_say(self, interaction_block=None):
        self.speech_handler.customized_say(interaction_block=interaction_block)

    # DIALOG
    def start_dialog(self, pid=0):
        self.pid = pid
        self.speech_handler.start_dialog()

    def stop_dialog(self):
        self.speech_handler.stop_dialog()
        if self.screen_handler is not None:
            self.screen_handler.set_webview(hide=True)
            self.screen_handler.set_image(hide=True)

        self.is_interacting = False
        self.pid = 0

    def pause_dialog(self):
        self.speech_handler.pause_dialog()

    def activate_topic(self, interaction_block):
        self.speech_handler.activate_topic(interaction_block)

    # TABLET:
    # -------
    def tablet(self, action_name=TabletAction.WEBVIEW, action_url="http://www.google.com", hide=False):
        if self.screen_handler is not None:
            try:
                if action_name is TabletAction.IMAGE:
                    self.screen_handler.set_image(image_path=action_url, hide=hide)
                elif action_name is TabletAction.WEBVIEW:
                    self.screen_handler.set_webview(webpage=action_url, hide=hide)
            except Exception as e:
                self.logger.error("Error while setting the tablet: {}".format(e))

    def load_application(self, app_name):
        if self.screen_handler is not None:
            self.screen_handler.load_application(app_name)

    def load_html_page(self, page_name="index"):
        self.speech_handler.raise_event(event_name="loadPage", event_value=page_name.lower())

    def get_distance(self, sonar=Sonar.FRONT):
        return self.sensor_handler.get_distance(sonar=sonar)
