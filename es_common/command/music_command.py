#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# =================== #
# MUSIC_COMMAND #
# =================== #
# Command for music player actions.
#
# @author ES
# **

import random
from collections import OrderedDict

from es_common.command.es_command import ESCommand
from es_common.enums.command_enums import ActionCommand


class MusicCommand(ESCommand):
    def __init__(self, command_type, playlist=None, track=None, play_time=-1):
        super(MusicCommand, self).__init__(command_type, is_speech_related=False)

        self.music_controller = None
        self.playlist = playlist
        self.track = track
        self.play_time = play_time  # -1 for playing the whole track

    # =======================
    # Override Parent methods
    # =======================
    def clone(self):
        return MusicCommand(ActionCommand.PLAY_MUSIC, playlist=self.playlist,
                            track=self.track, play_time=self.play_time)

    def reset(self):
        # TODO: reset the timer
        return "Not Implemented!"

    def execute(self):
        if self.music_controller is None or self.track is None:
            return False

        return self.music_controller.play(playlist=self.playlist, track=self.track)

    ###
    # SERIALIZATION
    ###
    def serialize(self):
        return OrderedDict([
            ("id", self.id),
            ("command_type", self.command_type.name),
            ("playlist", self.playlist),
            ("track", self.track),
            ("play_time", self.play_time)
        ])

    def deserialize(self, data, hashmap={}):
        self.id = data["id"]
        hashmap[data["id"]] = self

        self.playlist = data["playlist"]
        self.track = data["track"]

        self.play_time = data["play_time"] if "play_time" in data.keys() else -1

        return True
