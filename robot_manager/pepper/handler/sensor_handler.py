#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# ============== #
# SENSOR_HANDLER #
# ============== #
# Handler class for controlling the robot's sensors
#
# @author ES
# **

import logging

import es_common.hre_config as pconfig
from es_common.enums.led_enums import LedColor
from robot_manager.pepper.enums.sensor_enums import Sonar, LedName


class SensorHandler(object):

    def __init__(self, session):
        self.logger = logging.getLogger("Sensor Handler")

        self.memory = session.service("ALMemory")
        self.sonar = session.service("ALSonar")
        self.leds = session.service("ALLeds")

    def get_distance(self, sonar=Sonar.FRONT):
        return self.memory.getData(sonar.value)

    def set_leds(self, led_name=LedName.FACE, led_color=LedColor.WHITE, duration=0.5):
        self.leds.fadeRGB(led_name.value, led_color.r, led_color.g, led_color.b, duration)

    def led_animation(self, duration=2.0):
        self.leds.rasta(duration)
