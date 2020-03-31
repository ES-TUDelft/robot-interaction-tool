#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# ================ #
# ROBOT_CONTROLLER #
# ================ #
# Class for controlling the robot.
#
# @author ES
# **

import time
import logging
import functools

import es_common.hre_config as pconfig
from es_common.enums.led_enums import LedColor
from robot_manager.pepper.enums.motion_enums import HeadMotion, Animation, AutonomousLife
from robot_manager.pepper.enums.tablet_enums import TabletAction
from robot_manager.pepper.enums.sensor_enums import Sonar, LedName
from robot_manager.pepper.model.pepper_robot import PepperRobot
from es_common.utils.timer_helper import TimerHelper

import math


class RobotController(object):

    def __init__(self):
        self.logger = logging.getLogger(pconfig.logger_name)
        self.pepper_robot = None
        self.chat_agent = None
        self.image_viewer = None
        self.robot_id, self.last_time_touched = None, 0
        self.timer_helper = TimerHelper()

    def connect(self, robot_ip, port):
        self.pepper_robot = PepperRobot()
        return self.pepper_robot.connect(robot_ip=robot_ip, port=port)

    """
    Motion control methods
    """
    def posture(self, wakeup=False, reset=False):
        if self.pepper_robot is None:
            return False
        result = False
        try:
            self.pepper_robot.posture(wakeup=wakeup, reset=reset)
            result = True
            if reset is False:
                self.logger.info("Pepper is {}".format("awake" if wakeup is True else "resting"))
        except Exception as e:
            self.logger.error("Error while changing Pepper's posture")
            self.logger.error(e)
        finally:
            return result

    def breathing(self, enable=True):
        self.pepper_robot.breathing(enable=enable)
        self.logger.info("Breathing is {}".format("enabled" if enable is True else "disabled"))

    def engagement(self, is_engaged_signal, start=True):
        self.pepper_robot.engagement(is_engaged_signal, start=start)
        self.logger.info("Engagement is {}".format("enabled" if start is True else "disabled"))

    def is_interacting(self, value):
        self.pepper_robot.is_interacting = value

    def head(self, reset=False, motion=HeadMotion.YAW, angle=0.0, time=1.0):
        if reset is True:
            self.pepper_robot.head(reset=reset)
        else:
            # ang = self.pepper_robot.get_angles(joint = "Head", use_sensors=False)
            # self.logger.info("ANGLES = " + str(ang))
            # if math.fabs(math.fabs(ang[0]) - math.fabs(angle)) > 0.1:
            to_rotate = 0.0
            if motion._range[0] < angle < motion._range[1]:
                to_rotate = angle
            self.pepper_robot.head(motion=motion, angle=float(to_rotate), time=time)  # ang[0] - angle))

    def get_angles(self, joint="Body", use_sensors=True):
        return self.pepper_robot.get_angles(joint=joint, use_sensors=use_sensors)

    def animate(self, animation=Animation.WAVE):
        self.logger.info("At {} - Robot animation: {}".format(time.strftime("%H:%M:%S", time.localtime(time.time())),
                                                              animation.name))
        self.pepper_robot.animate(animation_name=animation)

    def execute_animation(self, animation_name):
        self.logger.info("At {} - Robot animation: {}".format(time.strftime("%H:%M:%S", time.localtime(time.time())),
                                                              animation_name))
        self.pepper_robot.execute_animation(animation_name=animation_name)

    def move_to(self, x=0, y=0, theta=0):
        self.pepper_robot.move_to(x=x, y=y, theta=theta)

    def move_and_animate(self, x=0, y=0, theta=0, message=None, animation=Animation.WAVE):
        self.logger.info(
            "At {} - Robot moves, waves and says: {}".format(time.strftime("%H:%M:%S", time.localtime(time.time())),
                                                             message))
        self.pepper_robot.move_and_animate(x=x, y=y, theta=theta, message=message, animation=animation)

    def led_animation(self, duration=1.0):
        self.pepper_robot.led_animation(duration=duration)

    def set_autonmous_life(self, state=AutonomousLife.DISABLED):
        self.pepper_robot.autonomous_life(state=state)

    def is_aware(self):
        return self.pepper_robot.is_aware()

    def awareness(self, enable=False):
        self.pepper_robot.awareness(enable=enable)

    def proxemics(self, value=0):
        delta_d = float(self.distance()) - value
        # self.logger.info("Delta_d = {}".format(delta_d))
        if abs(delta_d) > 0.1:  # define a threshold
            return delta_d
        return 0

    """
    TOUCH EVENTS
    """
    def touch(self):
        self.pepper_robot.subscribe_to_touch_events()
        self.robot_id = self.pepper_robot.touch.signal.connect(functools.partial(self.on_touch, "TouchChanged"))
        self.last_time_touched = time.time()
        self.logger.info("Touch is enabled")

    def on_touch(self, event_name, value):
        self.pepper_robot.touch.signal.disconnect(self.robot_id)

        if value[0][1] is True and (time.time() - self.last_time_touched) > 2:
            self.logger.info("Touched at: {}".format(value))
            self.last_time_touched = time.time()
            if value[0][0] == "Head":
                led_name = LedName.FACE
                message = 'Ay! Please, do not touch my head!'
            elif 'Base' in value[0][0] or 'Bumper' in value[0][0]:
                led_name = LedName.FACE
                message = 'Ay! Why did you kick me?'
            elif 'Arm' in value[0][0]:
                led_name = LedName.CHEST
                message = 'Ay! Please, do not touch my hands'
            else:
                led_name = LedName.CHEST
                message = 'Ay! Please, do not touch me again.'
            self.pepper_robot.react_to_touch(message=message, led_name=led_name, led_color_start=LedColor.RED,
                                             led_color_end=LedColor.WHITE)

        self.robot_id = self.pepper_robot.touch.signal.connect(functools.partial(self.on_touch, "TouchChanged"))

    """
    Speech control methods
    """
    def say(self, message=""):
        self.pepper_robot.say(message=message)
        self.logger.info(
            "At {} - Robot says: {}".format(time.strftime("%H:%M:%S", time.localtime(time.time())), message))

    def animated_say(self, message=None, animation_name=None):
        self.pepper_robot.animated_say(message=message, animation_name=animation_name)
        self.logger.info(
            "At {} - Robot says (with gesture): {}".format(time.strftime("%H:%M:%S", time.localtime(time.time())),
                                                           message))

    def customized_say(self, interaction_block=None):
        self.pepper_robot.customized_say(interaction_block=interaction_block)

    def set_volume(self, level=50.0):
        self.pepper_robot.volume(level=float(level) / 100)
        self.logger.info("Volume set to {}%".format(level))

    def set_language(self, language="English"):
        self.pepper_robot.language(name=language)
        time.sleep(1.0)  # To avoid a bug in naoqi set_language
        self.logger.info("Language set to '{}'".format(language))

    def start_dialog(self):
        self.pepper_robot.start_dialog()

    def stop_dialog(self):
        self.pepper_robot.stop_dialog()

    def pause_dialog(self):
        self.pepper_robot.pause_dialog()

    def activate_topic(self, interaction_block):
        self.pepper_robot.activate_topic(interaction_block=interaction_block)

    def tracking(self, enable=True):
        self.pepper_robot.tracking(enable=enable)

    def face_tracker(self, start=True, face_width=pconfig.default_face_width):
        self.pepper_robot.face_tracker(start=start, face_width=face_width)

    def divert_face_tracker(self, indexes=pconfig.divert_look_indexes, thresh=pconfig.divert_look_threshold,
                            gaze_pattern=None):
        self.pepper_robot.divert_look(indexes=indexes, thresh=thresh, gaze_pattern=gaze_pattern)

    def subscribe_to_dialog_events(self, block_completed_signal, user_answer_signal):
        self.pepper_robot.subscribe_to_dialog_events(block_completed_signal, user_answer_signal)

    """
    CHAT AGENT
    """
    # def activate_chat_agent(self):
    #     self.pepper_robot.subscribe_to_sound_detection()
    #     if self.chat_agent is None:
    #         self.chat_agent = RobotChatAgent()
    #         self.pepper_robot.subscribe_to_speech_events()
    #         self.robot_id = self.pepper_robot.last_input.signal.connect(functools.partial(self.on_speech))
    #         self.logger.info("### Chat is enabled")
    #
    # def on_speech(self, input):
    #     if input is None or input.strip() == '':
    #         return
    #     self.pepper_robot.last_input.signal.disconnect(self.robot_id)
    #
    #     self.logger.info("Pepper heard: {}".format(input))
    #     response = self.chat_agent.get_intent_from_text(input)
    #     self.pepper_robot.animated_say(message=response)
    #     # Subscribe to speech events
    #     self.robot_id = self.pepper_robot.last_input.signal.connect(functools.partial(self.on_speech))
    #
    # def set_sound_sensitivity(self, sensitivity=pconfig.sound_sensitivity):
    #     self.pepper_robot.sound_sensitivity(sensitivity=sensitivity)

    """
    Tablet control methods
    """
    def tablet_image(self, hide=True):
        self.pepper_robot.tablet(action_name=TabletAction.IMAGE, action_url=pconfig.welcome_image, hide=hide)

    def load_application(self, app_name):
        self.pepper_robot.load_application(app_name)

    def load_html_page(self, page_name="index"):
        self.pepper_robot.load_html_page(page_name=page_name)

    """
    LED CONTROL
    """
    def set_leds(self, led_name=LedName.FACE, led_color=LedColor.WHITE, duration=0.5):
        self.pepper_robot.set_leds(led_name=led_name, led_color=led_color)

    """
    SENSOR ACCESS
    """
    def distance(self, sonar=Sonar.FRONT):
        return self.pepper_robot.get_distance(sonar=sonar)

    # -------------- #
    # Helper Methods #
    # -------------- #
    def get_image_name(self):
        return "image_{}".format(time.time())

    def _get_fps(self):
        self.timer_helper.stop()
        fps = 1 / (self.timer_helper.end_time - self.timer_helper.start_time)
        return math.ceil(fps)
