#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# =================== #
# BINGO_COMMAND #
# =================== #
# Command for drawing bingo numbers.
# This is a special case of the DrawNumberCommand:
#   It returns letter-number combinations for a bingo game with:
#       min = 1, max = 75
#
# @author ES
# **
import logging
import random
from collections import OrderedDict

from es_common.command.draw_number_command import DrawNumberCommand
from es_common.enums.command_enums import ActionCommand


class BingoSpinnerCommand(DrawNumberCommand):
    def __init__(self, range_min=1, range_max=75):
        super(BingoSpinnerCommand, self).__init__(range_min=range_min, range_max=range_max)

        self.logger = logging.getLogger("Bingo Command")
        self.command_type = ActionCommand.BINGO_SPINNER

    # =======================
    # Override Parent methods
    # =======================
    def clone(self):
        return BingoSpinnerCommand()

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

        self.choices = data["choices"]
        self.prev_choices = data["prev_choices"]
        self.draw = data["draw"] if "draw" in data.keys() else self.prev_choices[len(self.prev_choices)-1]

        return True
