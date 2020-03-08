#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# ================== #
# ROBOT_CHAT_THREADS #
# ================== #
# Threads for controlling the robot chat
#
# @author ES
# **

import os
from os.path import expanduser

from PyQt5.QtCore import QThread, pyqtSignal
import logging
import time
import uuid

import es_common.hre_config as pconfig
from robot_manager.pepper.hre_modules.sound_processing_module import SoundProcessingModule
from es_common.enums.led_enums import LedColor
from robot_manager.pepper.hre_chat.robot_chat import RobotChatAgent
from robot_manager.pepper.hre_chat.chat_config import *
from robot_manager.pepper.hre_chat.detect_intent_stream import detect_intent_stream
import dialogflow_v2 as dialogflow

from google.api_core.exceptions import InvalidArgument
from google.oauth2 import service_account
from Queue import Queue  # Python 2 import


"""
ROBOT CHAT THREAD
"""


class RobotChatThread(QThread):
    chat_signal = pyqtSignal(dialogflow.types.QueryResult)
    led_color_signal = pyqtSignal(LedColor)

    def __init__(self, session):
        QThread.__init__(self)
        self.logger = logging.getLogger("ChatThread")
        self.session = session
        self.sound_processor = SoundProcessingModule(self.session)
        self.sound_processor.observers.append(self)
        self.service_id = None
        self.stop_chat = False
        self.chat_agent = RobotChatAgent()
        self.google_cloud = False
        self.peak = pconfig.sound_peak
        self.session_id = str(uuid.uuid4())

    def __del__(self):
        self.wait()

    def start_chat(self, google_cloud=False, peak=pconfig.sound_peak):
        if not self.isRunning():
            if self.service_id is None:
                self.service_id = self.session.registerService(self.sound_processor.module_name, self.sound_processor)
            self.google_cloud = google_cloud
            self.set_sound_peak(peak)
            self.stop_chat = False
            self.session_id = str(uuid.uuid4())
            self.sound_processor.start_processing()
            self.start()

    def pause_sound_processing(self, pause=True):
        self.sound_processor.pause_sound_processing = pause

    def set_sound_peak(self, peak):
        if peak < 0: return
        self.peak = peak
        self.sound_processor.set_sound_peak(peak)

    def run(self):
        while self.stop_chat is False:
            '''
            if self.sound_processor.audio_queue.empty() is False:
                audio = self.sound_processor.audio_queue.get()  # retrieve the next audio processing job from the queue
                input_text = self.recognize_speech(audio)
                self.logger.info("Input received: {}".format(input_text))
                if input_text is not None:
                    response = self.chat_agent.get_intent_from_text(text = input_text)
                    self.chat_signal.emit(time.time(), response)
                self.sound_processor.audio_queue.task_done() # mark the audio processing job as completed in the queue
            '''
            time.sleep(0.2)

        # STOP when a call to stop the chat is made
        self.sound_processor.stop_processing()
        self.session.unregisterService(self.service_id)

    def process_sound(self, audio=None, is_recording=False):
        if is_recording is True:
            self.led_color_signal.emit(LedColor.GREEN)
            return  # recording in progress...
        else:
            self.led_color_signal.emit(LedColor.WHITE)  # Stopped recording...

        if audio is None:
            return

        query_result = None
        try:
            if self.google_cloud is True:
                query_result = detect_intent_stream(DIALOGFLOW_PROJECT_ID, self.session_id, audio,
                                                    GOOGLE_CREDENTIALS_FROM_SERVICE_ACCOUNT, DIALOGFLOW_LANGUAGE_CODE)
                self.chat_signal.emit(query_result)
            else:
                # TODO: offline speech recognition
                self.logger.info("***Offline speech recognition is not configured***")
                pass
        except Exception as e:
            self.logger.error("Speech Recognizer error: {}".format(e))
