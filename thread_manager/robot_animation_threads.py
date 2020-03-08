#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# ======================= #
# ROBOT_ANIMATION_THREADS #
# ======================= #
# Threads for animating the robot
#
# @author ES
# **

import logging
import time

from PyQt5.QtCore import QThread, pyqtSignal

import es_common.hre_config as pconfig
from thread_manager.robot_engagement_threads import DialogThread
from robot_manager.pepper.controller.robot_controller import RobotController

# ------------------------ #
# THREADING HELPER CLASSES #
# ------------------------ #

"""
WAKE UP ROBOT THREAD
"""


class WakeUpRobotThread(QThread):
    awake_signal = pyqtSignal(bool)

    def __init__(self, robot_controller):
        QThread.__init__(self)
        self.robot_controller = RobotController() if robot_controller is None else robot_controller

    def __del__(self):
        self.wait()

    def run(self):
        is_awake = self.robot_controller.posture(wakeup=True)
        self.awake_signal.emit(is_awake)


"""
MOVE ROBOT THREAD
"""


class MoveRobotThread(QThread):
    movement_completed = pyqtSignal(bool)

    def __init__(self, robot_controller):
        QThread.__init__(self)
        self.robot_controller = RobotController() if robot_controller is None else robot_controller
        self.logger = logging.getLogger("MoveRobot Thread")
        self.x = 0
        self.y = 0,
        self.theta = 0

    def __del__(self):
        self.wait()

    def move_to(self, x=0, y=0, theta=0):
        self.x = x
        self.y = y
        self.theta = theta
        if not self.isRunning():
            self.run()

    def run(self):
        try:
            self.robot_controller.move_to(self.x, self.y, self.theta)
        except Exception as e:
            self.logger.error("Error while attempting to move the robot: {}".format(e))


"""
ROBOT ANIMATION THREAD
"""


class AnimateRobotThread(QThread):

    animation_completed = pyqtSignal(bool)
    dialog_started = pyqtSignal(bool)
    customized_say_completed = pyqtSignal(bool)
    customized_say_in_progress = pyqtSignal(bool)
    is_disconnected = pyqtSignal(bool)

    def __init__(self, robot_ip=pconfig.robot_ip, port=pconfig.naoqi_port):
        QThread.__init__(self)

        self.dialog_thread = None
        self.robot_controller = None

        # establish a connection with the robot
        self.connect_to_robot(robot_ip, port)

        self.logger = logging.getLogger("AnimateRobot Thread")
        self.animation = None
        self.message = None
        self.interaction_block = None
        self.behavioral_parameters = None
        self.is_first_block = True
        self.test_mode = False
        self.moving_enabled = False

    def connect_to_robot(self, robot_ip, port):
        self.robot_controller = RobotController()
        self.robot_controller.connect(robot_ip=robot_ip, port=port)
        if self.dialog_thread is not None:
            self.dialog_thread.robot_controller = self.robot_controller  # update controllers

        self._reset()

    def __del__(self):
        self.wait()

    def animate(self, animation):
        self.animation = animation
        if not self.isRunning():
            self.start()

    def animated_say(self, message=None, animation=None):
        self.message = message
        self.animation = animation
        if not self.isRunning():
            self.start()

    def customized_say(self, interaction_block=None, reset=False):
        if reset is True:
            self._reset()
            self.wait(10)
            self.logger.info("Recovered from waiting...")
            self.dialog(start=False)  # stop the dialog
        elif interaction_block:
            self.interaction_block = interaction_block
            if not self.isRunning():
                self.start()

    def _reset(self):
        self.robot_controller.posture(reset=True)
        self.move = False
        self.animation = None
        self.message = None
        self.interaction_block = None
        self.is_first_block = True
        self.test_mode = False

    def run(self):
        try:
            if self.interaction_block is None:
                return False

            self.interaction_block.interaction_start_time = time.time()

            # change eye colors
            self.robot_controller.set_leds(led_color=self.interaction_block.behavioral_parameters.eye_color,
                                           duration=0.5)

            # move robot to desired distance
            if self.moving_enabled is True:
                # proxemics
                delta_d = self.robot_controller.proxemics(value=self.interaction_block.behavioral_parameters.proxemics)
                if abs(delta_d) > 0:
                    # adjust the robot position
                    self.robot_controller.move_to(x=round(delta_d, 2))
                    self.logger.info("The robot is being asked to move for {}m.".format(round(delta_d, 2)))
                    # self.sleep(1)

            if self.test_mode is True:
                self.robot_controller.customized_say(interaction_block=self.interaction_block)
                self.customized_say(reset=True)
            else:
                # load the web application if it's the first block
                # TODO: use the "start" pattern as a trigger
                if self.is_first_block is True:
                    self.robot_controller.load_application(pconfig.app_name)
                    self.is_first_block = False

                # if a topic exists, active it; otherwise, say the message.
                if self.interaction_block.topic_tag.topic == "":
                    self.robot_controller.customized_say(interaction_block=self.interaction_block)
                    # update the time and emit the finished signal
                    self.interaction_block.interaction_end_time = time.time()
                    self.customized_say_completed.emit(True)
                else:
                    # start dialog thread if it's not running
                    if self.dialog_thread is None or (not self.dialog_thread.isRunning()):
                        self.dialog(start=True)  # if needed add: self.sleep(5)
                    # activate the topic
                    self.dialog_thread.activate_topic(self.interaction_block)
        except Exception as e:
            self.logger.error("Error: {}".format(e))
            self.dialog(start=False)
            if "socket" in "{}".format(e).lower():
                # self._connect_to_robot()
                self.logger.error("Robot is disconnected!")
                self.is_disconnected.emit(True)

    def dialog(self, start=False, pause=False):
        try:
            if start is True:
                if self.dialog_thread is None:
                    self.dialog_thread = DialogThread(self.robot_controller)
                    self.dialog_thread.dialog_started.connect(self.raise_dialog_started_event)
                    self.dialog_thread.block_completed.connect(self.raise_completed_event)
                self.dialog_thread.start_dialog()
            else:
                # no need to stop/pause dialog if it's none
                if self.dialog_thread is None:
                    return False
                # pause the dialog, if needed
                if pause is True:
                    self.dialog_thread.pause_dialog()
                else:  # stop the dialog
                    self.dialog_thread.stop_dialog = True
                    self.is_first_block = True
            return True
        except Exception as e:
            self.logger.error("Dialog error: {}".format(e))
            return False

    def raise_dialog_started_event(self, val):
        self.dialog_started.emit(True)

    def raise_completed_event(self, val):
        try:
            if self.test_mode is True:
                self.customized_say(reset=True)
            else:
                if self.interaction_block is not None:
                    self.interaction_block.interaction_end_time = time.time()
                self.dialog(start=False, pause=True)
                self.customized_say_completed.emit(True)
        except Exception as e:
            self.logger.error("Error: {}".format(e))
