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

import random

from es_common.command.draw_number_command import DrawNumberCommand
from es_common.enums.command_enums import ActionCommand


class BingoSpinnerCommand(DrawNumberCommand):
    def __init__(self, command_type):
        super(BingoSpinnerCommand, self).__init__(command_type, range_min=1, range_max=75)

        self.is_speech_related = True  # redundant!

    # =======================
    # Override Parent methods
    # =======================
    def clone(self):
        return BingoSpinnerCommand(ActionCommand.BINGO_SPINNER)

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
