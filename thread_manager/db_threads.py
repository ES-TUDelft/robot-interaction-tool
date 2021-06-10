#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# ======================= #
# DB_THREADS #
# ======================= #
# Threads for controlling DB Change Streams
#
# @author ES
# **

import os

import logging
import pymongo
from PyQt5.QtCore import QThread, pyqtSignal


class DBChangeStreamThread(QThread):

    def __init__(self):
        QThread.__init__(self)

        self.logger = logging.getLogger("DBChangeStream Thread")
        self.signals_dict = {} # contains the needed signals as pyqtSignals

        self.client = pymongo.MongoClient(os.environ['CHANGE_STREAM_DB'])
        self.db = self.client["InteractionBlocksDB"]
        self.robot_collection = self.db.collection["RobotCollection"]

        # self.pipeline = [{'$match': {'fullDocument.blockCompleted': 1}}]

    def __del__(self):
        self.wait()

    def start_listening(self):
        if not self.isRunning():
            self.start()

    def emit_signal(self, data):
        for key in data.keys():
            try:
                if key in self.signals_dict.keys():
                    self.signals_dict[key].emit(data[key])
            except Exception as e:
                self.logger.error("Error while emitting signal {} from {} | {}".format(data[key],
                                                                                       self.signals_dict[key], e))

    def run(self):
        change_stream = self.robot_collection.watch()

        for change in change_stream:
            data = change['fullDocument']
            print(data)
            self.emit_signal(data)
