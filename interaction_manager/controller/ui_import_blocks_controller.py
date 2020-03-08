#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# =========================== #
# UI_IMPORT_BLOCKS_CONTROLLER #
# =========================== #
# Class for controlling the blocks import editor GUI.
#
# @author ES
# **

import logging

from PyQt5 import QtGui, QtWidgets

import interaction_manager.utils.json_helper as json_helper
from interaction_manager.model.interaction_block import InteractionBlock
from interaction_manager.view.ui_import_blocks_dialog import Ui_ImportBlocksDialog


class UIImportBlocksController(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(UIImportBlocksController, self).__init__(parent)

        self.logger = logging.getLogger("ImportController")
        self.blocks = []

        # init UI elements
        self._init_ui()

        # give it control
        self.setModal(True)

    def _init_ui(self):
        self.ui = Ui_ImportBlocksDialog()
        self.ui.setupUi(self)

        # button listeners
        self.ui.selectFileToolButton.clicked.connect(self.select_file)

    def select_file(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select JSON file", "", "JSON Files (*.json)",
                                                             options=options)

        self.ui.fileNameLineEdit.setText(file_path)
        if file_path is None: return

        self.import_blocks()

    def import_blocks(self):
        error, message = (None,) * 2
        filename = self.ui.fileNameLineEdit.text()
        self.blocks = []

        if filename is None or filename == "":
            self.display_message(error="ERROR: Please select a file to import.")
            return

        blocks_data, error = json_helper.import_blocks(filename)
        if error is None:
            try:
                for _, block_dict in blocks_data.items():
                    self.blocks.append(InteractionBlock.create_interaction_block(block_dict=block_dict))
                message = "Data successfully imported (total of {} block(s)).".format(len(self.blocks))
            except Exception as e:
                error = "{} | {}".format("Error while importing data!" if error is None else error, e)
            finally:
                self.display_message(message=message, error=error)
        else:  # there was an error while reading the file
            self.display_message(error=error)

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
