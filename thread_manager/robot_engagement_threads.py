#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# ======================== #
# ROBOT_ENGAGEMENT_THREAD #
# ======================== #
# Threads for controlling the robot engagement and dialog
#
# @author ES
# **

import logging
import time

from PyQt5.QtCore import QThread, pyqtSignal

import es_common.hre_config as pconfig
from es_common.enums.speech_enums import GazePattern


# ------------------------ #
# THREADING HELPER CLASSES #
# ------------------------ #


class DialogThread(QThread):
    """
    ROBOT DIALOG THREAD
    """
    dialog_started = pyqtSignal(bool)
    block_completed = pyqtSignal(bool)
    stage_completed = pyqtSignal(bool)
    topic_completed = pyqtSignal(bool)

    def __init__(self, robot_controller):
        QThread.__init__(self)
        self.robot_controller = robot_controller
        self.robot_controller.subscribe_to_dialog_events(self.block_completed, self.stage_completed)
        self.stop_dialog = False
        self.logger = logging.getLogger(pconfig.logger_name)

    def __del__(self):
        self.wait()

    def start_dialog(self):
        if not self.isRunning():
            self.stop_dialog = False
            self.start()

    def pause_dialog(self):
        if self.isRunning():
            self.logger.info("Dialog paused.")
            self.robot_controller.pause_dialog()

    def activate_topic(self, dialogue_block):
        if self.isRunning():
            self.robot_controller.activate_topic(dialogue_block)
            # self.robot_controller.pepper_robot.speech_handler.block_completed.signal.connect(self.raise_block_completed_event)

    def raise_block_completed_event(self, val):
        self.logger.info("EVENT: {}".format(val))
        self.block_completed.emit(True)

    def exit_topic(self, val):
        self.topic_completed.emit(True)

    def run(self):
        self.robot_controller.start_dialog()
        self.dialog_started.emit(True)
        while self.stop_dialog is False:
            time.sleep(1)
        try:
            self.robot_controller.stop_dialog()
            self.robot_controller.posture(reset=True)
            self.logger.info("Stop dialog completed.")
        except Exception as e:
            self.logger.error("Error while stopping dialog: {}".format(e))


"""
ROBOT ENGAGEMENT THREAD
"""


class EngagementThread(QThread):
    is_engaged = pyqtSignal(bool)
    is_disconnected = pyqtSignal(bool)

    def __init__(self, robot_controller):
        QThread.__init__(self)
        self.robot_controller = robot_controller
        self.stop_engagement = False
        self.logger = logging.getLogger(pconfig.logger_name)

    def __del__(self):
        self.wait()

    def engagement(self, start=True):
        if start is False:
            self.stop_engagement = True
        elif (not self.isRunning()):
            self.start()

    def run(self):
        self.stop_engagement = False
        try:
            self.robot_controller.engagement(is_engaged_signal=self.is_engaged, start=True)
            while self.stop_engagement is False:
                time.sleep(1)

            self.robot_controller.engagement(is_engaged_signal=None, start=False)
            self.robot_controller.posture(reset=True)
        except Exception as e:
            self.is_disconnected.emit(True)
            self.logger.error("Error while connecting to the robot: {}".format(e))


"""
ROBOT FACE TRACKER THREAD
"""


class FaceTrackerThread(QThread):
    is_disconnected = pyqtSignal(bool)

    def __init__(self, robot_controller):
        QThread.__init__(self)
        self.robot_controller = robot_controller
        self.stop_tracking = False
        self.gaze_pattern = GazePattern.FIXATED
        self.tracking_start_time = 0
        self.logger = logging.getLogger(pconfig.logger_name)

    def __del__(self):
        self.wait()

    def track(self, start=True):
        if start is False:
            self.stop_tracking = True
        elif not self.isRunning():
            self.start()

    def run(self):
        self.stop_tracking = False
        try:
            self.robot_controller.face_tracker(start=True)
            self.gaze_pattern = GazePattern.FIXATED
            self.tracking_start_time = time.time()

            while self.stop_tracking is False:
                if ('DIVERTED' in self.gaze_pattern.name) and (
                        time.time() - self.tracking_start_time > pconfig.tracker_divert_time):
                    self.robot_controller.divert_face_tracker(gaze_pattern=self.gaze_pattern)
                    self.logger.info("*** Diverting gaze")
                    self.tracking_start_time = time.time()
                time.sleep(1)

            self.robot_controller.face_tracker(start=False)
            self.robot_controller.posture(reset=True)
        except Exception as e:
            # self.is_disconnected.emit(True)
            self.logger.error("Error: {}".format(e))
