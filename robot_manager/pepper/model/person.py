#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# ====== #
# PERSON #
# ====== #
# Class of a person model
#
# @author ES
# **

import logging
import time

import es_common.hre_config as pconfig
from robot_manager.pepper.enums.motion_enums import MovingStatus


class Person(object):
    def __init__(self, pid=None, is_new=True):
        self.logger = logging.getLogger("Person")
        self.is_new = is_new
        self.distance = 0
        self.moving_status = MovingStatus.UNKNOWN
        self.last_encounter = time.time()
        self.is_engaged = False
        self.is_warned = False
        self.pid = time.time() if pid is None else pid
        self.image_id = time.time()
        self.has_animation = None
        self.has_message = None

    @property
    def is_looking_at_camera(self):
        # TODO
        return False

    @property
    def to_string(self):
        return 'pid: {}, is new: {}, is looking at: {}, distance: {}, is engaged: {}, last encounter: {}'.format(
            self.pid, self.is_new, self.is_looking_at_camera, self.distance, self.is_engaged, self.last_encounter)

    @property
    def to_row(self):
        return {
            'pid': self.pid,
            'image_id': self.image_id,
            'is_new': None if self.is_new is False else True,
            'is_looking_at': None if self.is_looking_at_camera is False else True,
            'distance': "{0:.2f}".format(self.distance),
            'is_engaged': None if self.is_engaged is False else True,
            'has_animation': None if self.has_animation is None else self.has_animation.name,
            'has_message': None if self.has_message is None else self.has_message,
            'is_warned': None if self.is_warned is False else True,
            'last_encounter': self.last_encounter,
            'formatted_time': time.strftime("%H:%M:%S", time.localtime(self.last_encounter)),  # %a%d%b%Y_
        }

    @property
    def to_list(self):
        return [
            self.pid, self.is_new, self.is_looking_at_camera,
            self.distance, self.is_engaged, self.has_animation, self.has_message,
            self.last_encounter
        ]
