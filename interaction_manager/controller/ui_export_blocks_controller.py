#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# =========================== #
# UI_EXPORT_BLOCKS_CONTROLLER #
# =========================== #
# Class for controlling the blocks export editor GUI.
#
# @author ES
# **

import logging
import os
import time
from os.path import expanduser

from PyQt5 import QtGui, QtWidgets

import interaction_manager.utils.json_helper as json_helper
from interaction_manager.model.interaction_design import InteractionDesign
from interaction_manager.view.ui_export_blocks_dialog import Ui_ExportBlocksDialog


class UIExportBlocksController(QtWidgets.QDialog):

    def __init__(self, parent=None, interaction_design=None):
        super(UIExportBlocksController, self).__init__(parent)

        self.logger = logging.getLogger("ExportController")
        self.dialogue_design = InteractionDesign() if interaction_design is None else interaction_design

        # init UI elements
        self._init_ui()

        # give it control
        self.setModal(True)

    def _init_ui(self):
        self.ui = Ui_ExportBlocksDialog()
        self.ui.setupUi(self)
        # current directory
        self.ui.folderNameLineEdit.setText("{}/blocks".format(os.getcwd()))

        # file name
        self.ui.fileNameLineEdit.setText("{}Blocks_{}".format(self.dialogue_design.communication_style,
                                                              time.strftime("%d-%m-%y_%H-%M-%S", time.localtime())))

        # button listeners
        self.ui.selectFolderToolButton.clicked.connect(self.select_folder)
        self.ui.exportBlocksButton.clicked.connect(self.export_blocks)

    def select_folder(self):
        folder_name = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Select a folder",
            expanduser("~"),
            QtWidgets.QFileDialog.ShowDirsOnly
        )
        self.ui.folderNameLineEdit.setText(folder_name)

    def check_fields(self, foldername=None, filename=None):
        if foldername is None or foldername == "":
            self.display_message(error="ERROR: Please select a folder to save the file.")
            return False

        if filename is None or filename == "":
            self.display_message(error="ERROR: the file name is empty!")
            return False

        return True

    def export_blocks(self):
        filename = self.ui.fileNameLineEdit.text()
        foldername = self.ui.folderNameLineEdit.text()

        if self.check_fields(foldername=foldername, filename=filename) is False:
            return

        [message, error] = json_helper.export_blocks(filename=filename, foldername=foldername,
                                                     interaction_design=self.dialogue_design)
        self.display_message(message=message, error=error)

    def display_message(self, message=None, error=None):
        if message is None:
            self.ui.messageTextEdit.setTextColor(QtGui.QColor('red'))  # red text for errors
            self.ui.messageTextEdit.setText(error)
            self.logger.error(error)
        else:
            self.ui.messageTextEdit.setTextColor(QtGui.QColor('white'))
            self.ui.messageTextEdit.setText(message)
            self.logger.info(message)

        self.repaint()
