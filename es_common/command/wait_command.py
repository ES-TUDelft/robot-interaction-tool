#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# =================== #
# WAIT_COMMAND #
# =================== #
# Command for wait action.
#
# @author ES
# **
import logging
import random
from collections import OrderedDict

from PyQt5.QtCore import QTimer

from es_common.command.es_command import ESCommand
from es_common.enums.command_enums import ActionCommand


class WaitCommand(ESCommand):
    def __init__(self, command_type, wait_time=0):
        super(WaitCommand, self).__init__(command_type, is_speech_related=False)

        self.wait_time = wait_time

    # =======================
    # Override Parent methods
    # =======================
    def clone(self):
        return WaitCommand(ActionCommand.WAIT, wait_time=self.wait_time)

    def reset(self):
        # TODO: reset the timer
        return "Not Implemented!"

    def execute(self):
        # QTimer.singleShot(self.wait_time * 1000, self.on_finish)
        return True

    def on_finish(self):
        self.logger.debug("Finished waiting for {} seconds".format(self.wait_time))
        return True

    ###
    # SERIALIZATION
    ###
    def serialize(self):
        return OrderedDict([
            ("id", self.id),
            ("command_type", self.command_type.name),
            ("wait_time", self.wait_time)
        ])

    def deserialize(self, data, hashmap={}):
        self.id = data["id"]
        hashmap[data["id"]] = self

        self.wait_time = data["wait_time"] if "wait_time" in data.keys() else 0

        return True
