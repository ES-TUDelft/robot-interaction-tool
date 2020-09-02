#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# =================== #
# DRAW_NUMBER_COMMAND #
# =================== #
# Command for drawing numbers from a range.
#
# @author ES
# **
import logging
import random
from collections import OrderedDict

from es_common.command.es_command import ESCommand
from es_common.enums.command_enums import ActionCommand


class DrawNumberCommand(ESCommand):
    def __init__(self, range_min=None, range_max=None):
        super(DrawNumberCommand, self).__init__(is_speech_related=True)

        self.logger = logging.getLogger("DrawNumber Command")
        self.command_type = ActionCommand.DRAW_NUMBER
        self.range_min = int(range_min) if range_min is not None else 0
        self.range_max = int(range_max) if range_max is not None else 10
        self._verify_range()
        self.draw = 0

        self.choices = []
        self.prev_choices = []
        self.reset()

    def _verify_range(self):
        if self.range_min > self.range_max:  # flip
            tmp = self.range_min
            self.range_min = self.range_max
            self.range_max = tmp

    # =======================
    # Override Parent methods
    # =======================
    def clone(self):
        return DrawNumberCommand(range_min=self.range_min, range_max=self.range_max)

    def reset(self):
        self.choices = [i for i in range(self.range_min, self.range_max)]
        self.prev_choices = []
        self.draw = 0

    def execute(self):
        if len(self.choices) == 0:
            self.reset()

        draw = random.choice(self.choices)
        self.choices.remove(draw)
        self.prev_choices.append(draw)

        return draw

    ###
    # SERIALIZATION
    ###
    def serialize(self):
        return OrderedDict([
            ("id", self.id),
            ("command_type", self.command_type.name),
            ("range_min", self.range_min),
            ("range_max", self.range_max),
            ("draw", self.draw),
            ("choices", self.choices),
            ("prev_choices", self.prev_choices)
        ])

    def deserialize(self, data, hashmap={}):
        self.id = data["id"]
        hashmap[data["id"]] = self

        self.range_min = data["range_min"]
        self.range_max = data["range_max"]

        self.choices = data["choices"]
        self.prev_choices = data["prev_choices"]
        self.draw = data["draw"] if "draw" in data.keys() else self.prev_choices[len(self.prev_choices)-1]

        return True
