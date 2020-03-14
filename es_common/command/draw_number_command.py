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

import random
from collections import OrderedDict

from es_common.command.es_command import ESCommand
from interaction_manager.utils import config_helper


class DrawNumberCommand(ESCommand):
    def __init__(self, command_type, range_min=None, range_max=None):
        super(DrawNumberCommand, self).__init__(command_type)

        self.range_min = int(range_min) if range_min is not None else 0
        self.range_max = int(range_max) if range_max is not None else 10
        self._verify_range()

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

        return True
