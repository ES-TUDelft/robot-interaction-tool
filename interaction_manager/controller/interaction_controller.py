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
import time

import es_common.hre_config as pconfig
from es_common.model.observable import Observable
from robot_manager.pepper.controller.robot_controller import RobotController
from thread_manager.robot_animation_threads import WakeUpRobotThread, AnimateRobotThread
from thread_manager.robot_engagement_threads import EngagementThread, FaceTrackerThread


class InteractionController(object):
    def __init__(self, block_controller):
        self.logger = logging.getLogger("Interaction Controller")

        self.block_controller = block_controller
        self.robot_controller = None
        self.wakeup_thread = None
        self.animation_thread = None
        self.engagement_thread = None
        self.face_tracker_thread = None

        self.robot_ip = None
        self.port = None

        self.engagement_counter = 0
        self.is_ready_to_interact = False
        self.current_interaction_block = None
        self.previous_interaction_block = None
        self.interaction_blocks = None
        self.interaction_design = None

        self.stop_playing = False
        self.execution_result = None
        self.has_finished_playing_observable = Observable()

    def connect_to_robot(self, robot_ip, port):
        self.robot_ip = robot_ip
        self.port = port

        pconfig.robot_ip = self.robot_ip
        pconfig.naoqi_port = self.port

        self.robot_controller = RobotController()

        message, error, is_awake = self.robot_controller.connect(robot_ip=self.robot_ip, port=self.port)

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

    def update_threads(self, enable_moving=False):
        if self.animation_thread is None:
            self.animation_thread = AnimateRobotThread(robot_ip=self.robot_ip, port=self.port)
            self.animation_thread.dialog_started.connect(self.engagement)
            self.animation_thread.customized_say_completed.connect(self.customized_say)

            # TODO: check enable moving from the ui, e.g., self.ui.enableMovingCheckBox.isChecked()
            self.animation_thread.moving_enabled = enable_moving
            self.animation_thread.is_disconnected.connect(self.disconnect_from_robot)
        else:
            self.animation_thread.connect_to_robot(robot_ip=self.robot_ip,
                                                   port=self.port)

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
    def animate(self, animation=None):
        self.animation_thread.animate(animation=animation)

    def animated_say(self, message=None, animation=None):
        self.animation_thread.animated_say(message=message, animation=animation)

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

    def customized_say(self):
        while self.animation_thread.isRunning():
            self.logger.debug("*** Animation Thread is still running!")
            time.sleep(1)  # wait for the thread to finish

        self.block_controller.clear_selection()

        connecting_edge = None
        if self.previous_interaction_block is None:  # interaction has just started
            self.previous_interaction_block = self.current_interaction_block
        else:  # playing is in progress
            # get the next block to say
            self.current_interaction_block, connecting_edge = self.get_next_interaction_block()

        # if there are no more blocks, stop interacting
        if self.current_interaction_block is None or self.stop_playing is True:
            self.animation_thread.customized_say(reset=True)
            # stop interacting
            self.interaction(start=False)

            self.tablet_image(hide=False)
        else:
            # execute the block
            self.current_interaction_block.set_selected(True)
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

            # update previous block
            # self.previous_block = self.current_block

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
