#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# =========================== #
# DATABASE_CONTROLLER #
# =========================== #
# Class for managing the interaction flow with the robot.
#
# @author ES
# **

import logging

from PyQt5.QtCore import QTimer

import es_common.hre_config as pconfig
from es_common.enums.command_enums import ActionCommand
from es_common.model.observable import Observable
from es_common.utils.timer_helper import TimerHelper
from block_manager.enums.block_enums import ExecutionMode
from interaction_manager.utils import config_helper
from robot_manager.pepper.controller.robot_controller import RobotController
from thread_manager.robot_animation_threads import WakeUpRobotThread, AnimateRobotThread
from thread_manager.robot_engagement_threads import EngagementThread, FaceTrackerThread


class InteractionController(object):
    def __init__(self, block_controller, music_controller=None):
        self.logger = logging.getLogger("Interaction Controller")

        self.block_controller = block_controller
        self.music_controller = music_controller
        self.robot_controller = None
        self.wakeup_thread = None
        self.animation_thread = None
        self.engagement_thread = None
        self.face_tracker_thread = None
        self.timer_helper = TimerHelper()
        self.music_command = None
        self.animations_lst = []
        self.animation_time = 0
        self.animation_counter = -1
        self.robot_volume = 50

        self.robot_ip = None
        self.port = None
        self.robot_name = None

        self.engagement_counter = 0
        self.is_ready_to_interact = False
        self.current_interaction_block = None
        self.previous_interaction_block = None
        self.interaction_blocks = None
        self.interaction_design = None

        self.stop_playing = False
        self.execution_result = None
        self.has_finished_playing_observable = Observable()

    def connect_to_robot(self, robot_ip, port, robot_name=None):
        self.robot_ip = robot_ip
        self.port = port
        self.robot_name = robot_name

        pconfig.robot_ip = self.robot_ip
        pconfig.naoqi_port = self.port

        self.robot_controller = RobotController()

        message, error, is_awake = self.robot_controller.connect(robot_ip=self.robot_ip,
                                                                 port=self.port,
                                                                 robot_name=self.robot_name)

        self.update_threads()

        return message, error, is_awake

    def disconnect_from_robot(self):
        self.engagement_counter = 0
        try:
            if self.animation_thread is not None:
                self.engagement(start=False)
        except Exception as e:
            self.logger.error("Error while disconnecting from robot. | {}".format(e))
        finally:
            self.robot_controller = None

        # if self.animation_thread is not None:
        #     self.animation_thread.dialog(start=False)
        return True

    def is_connected(self):
        return False if self.robot_controller is None else True

    def update_threads(self, enable_moving=False):
        if self.animation_thread is None:
            self.animation_thread = AnimateRobotThread(robot_ip=self.robot_ip, port=self.port,
                                                       robot_name=self.robot_name)
            self.animation_thread.dialog_started.connect(self.engagement)
            self.animation_thread.customized_say_completed.connect(self.customized_say)
            self.animation_thread.animation_completed.connect(self.on_animation_completed)

            # TODO: check enable moving from the ui, e.g., self.ui.enableMovingCheckBox.isChecked()
            self.animation_thread.moving_enabled = enable_moving
            self.animation_thread.is_disconnected.connect(self.disconnect_from_robot)
        else:
            self.animation_thread.connect_to_robot(robot_ip=self.robot_ip,
                                                   port=self.port,
                                                   robot_name=self.robot_name)

        if self.face_tracker_thread is None:
            self.face_tracker_thread = FaceTrackerThread(robot_controller=self.robot_controller)
            self.face_tracker_thread.is_disconnected.connect(self.disconnect_from_robot)
        else:
            # update the robot controller
            self.face_tracker_thread.robot_controller = self.robot_controller

        if self.engagement_thread is None:
            self.engagement_thread = EngagementThread(robot_controller=self.robot_controller)
            self.engagement_thread.is_engaged.connect(lambda: self.interaction(start=True))
            self.engagement_thread.is_disconnected.connect(self.disconnect_from_robot)
        else:
            # update the robot controller
            self.engagement_thread.robot_controller = self.robot_controller

    def wakeup_robot(self):
        success = False
        try:
            self.wakeup_thread = WakeUpRobotThread(robot_controller=self.robot_controller)
            self.wakeup_thread.start()
            success = True
        except Exception as e:
            self.logger.error("Error while waking up the robot! | {}".format(e))
        finally:
            return success

    def rest_robot(self):
        return self.robot_controller.posture(wakeup=False)

    # TOUCH
    # ------
    def enable_touch(self):
        self.robot_controller.touch()

    # TRACKING
    # ---------
    def tracking(self, enable=True):
        self.robot_controller.tracking(enable=enable)

    # BEHAVIORS
    # ---------
    def animate(self, animation_name=None):
        self.animation_thread.animate(animation_name=animation_name)

    def animated_say(self, message=None, animation_name=None):
        self.animation_thread.animated_say(message=message, animation_name=animation_name)

    # SPEECH
    # ------
    def say(self, message=None):
        to_say = "Hello!" if message is None else message
        if message is None:
            self.logger.info(to_say)
        self.animated_say(message=to_say)

    def start_playing(self, int_block, engagement_counter=0):
        if int_block is None:
            return False

        self.stop_playing = False
        self.previous_interaction_block = None
        self.current_interaction_block = int_block
        self.current_interaction_block.execution_mode = ExecutionMode.NEW
        self.logger.debug("Started playing the blocks")

        # set the engagement counter
        self.engagement_counter = int(engagement_counter)  # int(self.ui.enagementRepetitionsSpinBox.value())

        # ready to interact
        self.is_ready_to_interact = True

        # self.animation_thread.robot_controller.posture(reset = True)
        if self.animation_thread.dialog_thread is None or (not self.animation_thread.dialog_thread.isRunning()):
            self.animation_thread.dialog(start=True)
            self.logger.info("Called dialog to start!")

        # start engagement
        self.engagement(start=True)
        return True

    def get_next_interaction_block(self):
        if self.current_interaction_block is None:
            return None

        next_block = None
        connecting_edge = None
        self.logger.debug("Getting the next interaction block...")
        try:
            self.logger.debug("Execution Result: {}".format(self.animation_thread.execution_result))

            next_block, connecting_edge = self.current_interaction_block.get_next_interaction_block(
                execution_result=self.animation_thread.execution_result)

            # complete execution
            self.current_interaction_block.execution_mode = ExecutionMode.COMPLETED

            # update previous block
            self.previous_interaction_block = self.current_interaction_block
        except Exception as e:
            self.logger.error("Error while getting the next block! {}".format(e))
        finally:
            return next_block, connecting_edge

    def interaction(self, start):
        self.logger.info("Interaction called with start = {}".format(start))

        if start is False:  # stop the interaction
            self.tablet_image(hide=True)
            self.robot_controller.is_interacting(False)

            self.is_ready_to_interact = False
            self.interaction_blocks = []  # empty the blocks
            self.engagement(start=False)

            return "Successfully stopped the interaction"

        elif self.is_ready_to_interact is True:  # start is True
            self.robot_controller.is_interacting(start)
            self.customized_say()  # start interacting

    def stop_engagement_callback(self):
        # stop!
        self.engagement_counter = 0
        self.interaction(start=False)

    def engagement(self, start):
        """
        @param start = bool
        """
        self.logger.info("Engagement called with start = {} and counter = {}".format(start, self.engagement_counter))
        if start is True:
            self.engagement_thread.engagement(start=True)
            self.face_tracker_thread.track(start=True)
        else:
            # decrease the engagement counter
            self.engagement_counter -= 1
            # stop the engagement if the counter is <= 0
            if self.engagement_counter <= 0:
                self.animation_thread.dialog(start=False)
                self.engagement_thread.engagement(start=False)
                self.face_tracker_thread.track(start=False)

                self.has_finished_playing_observable.notify_all(True)
                # TODO: move to ui
                # self._enable_buttons([self.ui.actionPlay], enabled=True)
                # self._enable_buttons([self.ui.actionStop], enabled=False)

            else:  # continue
                self.animation_thread.dialog(start=False, pause=True)
                # ready to interact
                self.is_ready_to_interact = True

    def verify_current_interaction_block(self):
        # if there are no more blocks, stop interacting
        if self.current_interaction_block is None or self.stop_playing is True:
            self.animation_thread.customized_say(reset=True)
            # stop interacting
            self.interaction(start=False)

            self.tablet_image(hide=True)
            return False
        return True

    def customized_say(self):
        if self.verify_current_interaction_block() is False:
            return False

        if self.animation_thread.isRunning():
            self.logger.debug("*** Animation Thread is still running!")
            return QTimer.singleShot(1000, self.customized_say)  # wait for the thread to finish

        self.block_controller.clear_selection()
        connecting_edge = None

        # check for remaining actions
        if self.execute_action_command() is True:
            return True

        if self.previous_interaction_block is None:  # interaction has just started
            self.previous_interaction_block = self.current_interaction_block
        else:
            # get the next block to say
            self.current_interaction_block, connecting_edge = self.get_next_interaction_block()
            if self.verify_current_interaction_block() is False:
                return False

        # execute the block
        self.current_interaction_block.execution_mode = ExecutionMode.EXECUTING
        self.current_interaction_block.set_selected(True)
        self.current_interaction_block.volume = self.robot_volume

        if connecting_edge is not None:
            connecting_edge.set_selected(True)

        # TODO: set the block state to 'executing'
        # set the tracker's gaze pattern
        if not self.face_tracker_thread.isRunning():
            self.face_tracker_thread.track()
        self.face_tracker_thread.gaze_pattern = self.current_interaction_block.behavioral_parameters.gaze_pattern

        # get the result from the execution
        self.animation_thread.customized_say(interaction_block=self.current_interaction_block)

        self.logger.debug("Robot: {}".format(self.current_interaction_block.message))
        return True

    def execute_action_command(self):
        # check for remaining actions
        if self.current_interaction_block.execution_mode is ExecutionMode.EXECUTING:
            if self.current_interaction_block.has_action(action_type=ActionCommand.PLAY_MUSIC):
                self.on_music_mode()
                return True
            elif self.current_interaction_block.has_action(action_type=ActionCommand.WAIT):
                self.on_wait_mode()
                return True

        return False

    def on_wait_mode(self):
        wait_time = 1  # 1s
        try:
            if self.current_interaction_block is not None:
                self.current_interaction_block.execution_mode = ExecutionMode.COMPLETED
                wait_command = self.current_interaction_block.action_command
                if wait_command is not None:
                    wait_time = wait_command.wait_time
        except Exception as e:
            self.logger.error("Error while setting wait time! {}".format(e))
        finally:
            self.logger.debug("Waiting for {} s".format(wait_time))
            QTimer.singleShot(wait_time * 1000, self.customized_say)

    def on_music_mode(self):
        if self.music_controller is None:
            self.logger.debug("Music player is not connected! Will skip playing music.")
            self.on_music_stop()
        else:
            self.current_interaction_block.action_command.music_controller = self.music_controller
            success = self.current_interaction_block.action_command.execute()
            if success is True:
                self.logger.debug("Playing now: {}".format(self.current_interaction_block.action_command.track))
                # TODO: specify wait time as track time when play_time is < 0
                # use action play time
                wait_time = self.current_interaction_block.action_command.play_time
                if wait_time <= 0:
                    wait_time = 30  # wait for 30s then continue
                anim_key = self.current_interaction_block.action_command.animations_key
                if anim_key is None or anim_key == "":
                    QTimer.singleShot(int(wait_time) * 1000, self.on_music_stop)
                else:
                    self.on_animation_mode(music_command=self.current_interaction_block.action_command,
                                           animation_time=int(wait_time))
                # QTimer.singleShot(wait_time * 1000, self.on_music_stop)
            else:
                self.logger.warning("Unable to play music! {}".format(self.music_controller.warning_message))
                self.on_music_stop()

    def on_animation_mode(self, music_command, animation_time=0):
        self.music_command = music_command
        self.animations_lst = config_helper.get_animations()[music_command.animations_key]
        self.animation_time = animation_time
        self.animation_counter = -1

        self.timer_helper.start()
        self.execute_next_animation()

    def on_animation_completed(self):
        if self.animation_thread.isRunning():
            self.logger.debug("*** Animation Thread is still running!")
            QTimer.singleShot(2000, self.on_animation_completed)  # wait for the thread to finish
        else:
            QTimer.singleShot(3000, self.execute_next_animation)

    def execute_next_animation(self):
        if self.music_command is None or len(self.animations_lst) == 0:
            QTimer.singleShot(1000, self.on_music_stop)
        elif self.timer_helper.elapsed_time() <= self.animation_time - 4:  # use 4s threshold
            # repeat the animations if the counter reached the end of the lst
            self.animation_counter += 1
            if self.animation_counter >= len(self.animations_lst):
                self.animation_counter = 0
            animation, message = self.get_next_animation(self.animation_counter)
            if message is None or message == "":
                self.animation_thread.animate(animation_name=animation)
            else:
                self.animation_thread.animated_say(message=message,
                                                   animation_name=animation,
                                                   robot_voice=self.get_robot_voice())
        else:
            remaining_time = self.animation_time - self.timer_helper.elapsed_time()
            QTimer.singleShot(1000 if remaining_time < 0 else remaining_time * 1000, self.on_music_stop)

    def get_next_animation(self, anim_index):
        anim, msg = ("", "")
        try:
            animation_dict = self.animations_lst[anim_index]
            if len(animation_dict) > 0:
                anim = animation_dict.keys()[0]
                msg = animation_dict[anim]
        except Exception as e:
            self.logger.error("Error while getting next animation! {}".format(e))
        finally:
            return anim, msg

    def get_robot_voice(self):
        if self.current_interaction_block is None:
            return None

        return self.current_interaction_block.behavioral_parameters.voice

    def on_music_stop(self):
        self.logger.debug("Finished playing music.")
        try:
            if self.current_interaction_block is not None:
                self.current_interaction_block.execution_mode = ExecutionMode.COMPLETED
            if self.music_controller is not None:
                self.music_controller.pause()
        except Exception as e:
            self.logger.error("Error while stopping the music! {}".format(e))
        finally:
            self.customized_say()

    def test_behavioral_parameters(self, interaction_block, behavioral_parameters, volume):
        message, error = (None,) * 2

        if self.robot_controller is None:
            error = "Please connect to the robot to be able to test the parameters."
        else:
            b = interaction_block.clone()
            b.behavioral_parameters = behavioral_parameters
            b.behavioral_parameters.speech_act = interaction_block.speech_act.clone()
            b.behavioral_parameters.voice.volume = volume

            self.face_tracker_thread.gaze_pattern = b.behavioral_parameters.gaze_pattern
            self.animation_thread.test_mode = True
            self.animation_thread.customized_say(interaction_block=b)
            message = "Testing: {}".format(b.message)

        return message, error

    # TABLET
    # ------
    def tablet_image(self, hide=False):
        self.robot_controller.tablet_image(hide=hide)

    # MOVEMENT
    # --------
    def enable_moving(self):
        if self.animation_thread is None:
            return

        self.animation_thread.moving_enabled = self.ui.enableMovingCheckBox.isChecked()
        self.logger.info("#### MOVING: {}".format(self.animation_thread.moving_enabled))
