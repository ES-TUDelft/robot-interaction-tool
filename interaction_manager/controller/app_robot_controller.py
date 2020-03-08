#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# ==================== #
# APP_ROBOT_CONTROLLER #
# ==================== #
# Class for controlling the robot.
#
# @author ES
# **

from robot_manager.pepper.controller.robot_controller import RobotController


class AppRobotController(RobotController):
    def __init__(self):
        super(AppRobotController, self).__init__()
