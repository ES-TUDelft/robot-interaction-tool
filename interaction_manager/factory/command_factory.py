#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# =========== #
# COMMAND_FACTORY #
# =========== #
# Factory for creating commands.
#
# @author ES
# **
from es_common.command.bingo_spinner_command import BingoSpinnerCommand
from es_common.command.draw_number_command import DrawNumberCommand
from es_common.enums.command_enums import ActionCommand
from interaction_manager.utils import config_helper


class CommandFactory(object):

    @staticmethod
    def create_command(command_type, *args):
        new_command = None
        try:
            if command_type is ActionCommand.DRAW_NUMBER:
                new_command = DrawNumberCommand(command_type, *args)
            elif command_type is ActionCommand.BINGO_SPINNER:
                new_command = BingoSpinnerCommand(command_type)

        except Exception as e:
            config_helper.logger.error("Error while creating command: {} | {}".format(command_type, e))
        finally:
            return new_command
