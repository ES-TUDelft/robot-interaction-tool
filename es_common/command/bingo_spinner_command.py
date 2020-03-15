#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# =================== #
# BINGO_COMMAND #
# =================== #
# Command for drawing bingo numbers.
#
# @author ES
# **

import random
from collections import OrderedDict

from es_common.command.es_command import ESCommand
from es_common.enums.command_enums import ActionCommand


class BingoSpinnerCommand(ESCommand):
    def __init__(self, command_type):
        super(BingoSpinnerCommand, self).__init__(command_type)

        self.range_min = 1
        self.range_max = 75
        self.draw = 0

        self.choices = []
        self.prev_choices = []
        self.reset()

    # =======================
    # Override Parent methods
    # =======================
    def clone(self):
        return BingoSpinnerCommand(ActionCommand.BINGO_SPINNER)

    def reset(self):
        self.choices = [i for i in range(self.range_min, self.range_max)]
        self.prev_choices = []
        self.draw = 0

    def execute(self):
        if len(self.choices) == 0:
            self.reset()

        self.draw = random.choice(self.choices)
        self.choices.remove(self.draw)
        self.prev_choices.append(self.draw)

        return self.get_number_letter_combination()

    def get_number_letter_combination(self):
        """
        B: [1, 15]
        I: [16, 30]
        N: [31, 45]
        G: [46, 60]
        O: [61, 75]
        :return: number letter combination or 0 otherwise.
        """
        if self.draw <= 0:
            return self.draw

        if self.draw <= 15:
            return "B {}".format(self.draw)

        if self.draw <= 30:
            return "I {}".format(self.draw)

        if self.draw <= 45:
            return "N {}".format(self.draw)

        if self.draw <= 60:
            return "G {}".format(self.draw)

        # draw <= 75
        return "O {}".format(self.draw)

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

        self.draw = data["draw"]
        self.choices = data["choices"]
        self.prev_choices = data["prev_choices"]

        return True
