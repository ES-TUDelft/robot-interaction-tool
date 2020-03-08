#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# ============================== #
# UI_ROBOT_CONNECTION_CONTROLLER #
# ============================== #
# Class for controlling the robot connection editor GUI.
#
# @author ES
# **

import logging

from PyQt5 import QtCore, QtWidgets, QtGui

import es_common.hre_config as pconfig
from interaction_manager.view.ui_connection_dialog import Ui_ConnectionDialog
from es_common.utils import ip_helper


class UIRobotConnectionController(QtWidgets.QDialog):

    def __init__(self, interaction_controller, parent=None):
        super(UIRobotConnectionController, self).__init__(parent)

        self.logger = logging.getLogger("UIRobotConnection Controller")

        self.interaction_controller = interaction_controller
        self.robot_ip = None
        self.robot_port = None
        self.is_awake = False

        self.success = False

        # init UI elements
        self._init_ui()

        # give it control
        self.setModal(True)

    def _init_ui(self):
        self.ui = Ui_ConnectionDialog()
        self.ui.setupUi(self)

        # Set validator and field for IP address
        self._set_ip_validator(self.ui.robotIPValue)
        self._set_ip_field(self.ui.robotIPValue)
        # connect listener
        self.ui.connectPushButton.clicked.connect(self.connect)

        if self.interaction_controller is None:
            self.ui.connectPushButton.setEnabled(False)
            self._display_message(error="Unable to connect to robot! Try again later.")

        self.repaint()

    def connect(self):
        self.success = False

        self.robot_ip = str(self.ui.robotIPValue.text()).strip()
        self.robot_port = str(self.ui.robotPortValue.text()).strip()

        self.logger.info("IP: {} - PORT: {}".format(self.robot_ip, self.robot_port))

        self._display_message(message="Connecting...")

        message, error, self.is_awake = self.interaction_controller.connect_to_robot(robot_ip=self.robot_ip,
                                                                                     port=self.robot_port)
        if self.error is None:
            self.success = True
            self.ui.connectPushButton.setEnabled(False)
        else:
            self.success = False
            error = "Please enter a valid IP and PORT | {}".format(error)

        self._display_message(message=message, error=error)

    def _display_message(self, message=None, error=None):
        if message is None:
            self.ui.messageTextEdit.setTextColor(QtGui.QColor('red'))  # red text for errors
            self.ui.messageTextEdit.setText(error)
            self.logger.error(error)
        else:
            self.ui.messageTextEdit.setTextColor(QtGui.QColor('white'))
            self.ui.messageTextEdit.setText(message)
            self.logger.info(message)

        self.repaint()

    # ------------------------------------- #
    # Methods for Getting/Setting UI Values #
    # ------------------------------------- #
    """
    ROBOT IP
    """

    @property
    def robot_ip(self):
        return self.__robot_ip

    @robot_ip.setter
    def robot_ip(self, value):
        self.__robot_ip = pconfig.robot_ip if (value is None or str(value).strip() == '') else str(value).strip()

    @property
    def robot_port(self):
        return self.__robot_port

    @robot_port.setter
    def robot_port(self, value):
        self.__robot_port = pconfig.naoqi_port if (value is None or str(value).strip() == '') else str(value).strip()

    # -------------- #
    # Helper Methods #
    # -------------- #
    def _set_ip_validator(self, line_edit):
        """
        @param line_edit of type QLineEdit
        """
        _range = '(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])'  # [0, 255]
        reg_ex = QtCore.QRegExp(r'^' + _range + '\\.' + _range + '\\.' + _range + '\\.' + _range + '$')
        ip_validator = QtGui.QRegExpValidator(reg_ex, line_edit)  # self.ui.robotIPValue)
        line_edit.setValidator(ip_validator)

    def _set_ip_field(self, line_edit):
        """
        @param line_edit of type QLineEdit
        """
        try:
            ip_parts = (ip_helper.get_host_ip()).split('.')
            line_edit.setText('{}.{}.{}.{}'.format(ip_parts[0], ip_parts[1], ip_parts[2], 0))
        except Exception as e:
            self._display_message(error="Error while getting the router IP!\n{}".format(e))
