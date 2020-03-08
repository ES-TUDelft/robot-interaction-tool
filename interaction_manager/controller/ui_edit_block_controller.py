#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# ========================= #
# UI_EDIT_BLOCK_CONTROLLER #
# ========================= #
# Class for controlling the block editor GUI.
#
# @author ES
# **

import logging

from PyQt5 import QtCore, QtWidgets

from interaction_manager.utils import config_helper
import es_common.hre_config as pconfig
from interaction_manager.model.interaction_block import InteractionBlock
from interaction_manager.model.speech_act import SpeechAct
from interaction_manager.view.ui_editblock_dialog import Ui_EditBlockDialog
from es_common.model.tablet_page import TabletPage
from es_common.model.topic_tag import TopicTag


class UIEditBlockController(QtWidgets.QDialog):
    def __init__(self, parent=None, interaction_block=None):
        super(UIEditBlockController, self).__init__(parent)

        self.logger = logging.getLogger("EditBlockController")

        # init UI elements
        self.ui = Ui_EditBlockDialog()
        self.ui.setupUi(self)

        self.interaction_block = interaction_block

        # init ui elements
        self._init_ui()

        # give it control
        self.setModal(True)

    def _init_ui(self):
        if self.interaction_block is None:
            self.interaction_block = InteractionBlock()

        self.setWindowTitle("Edit Block")

        # block properties
        self.ui.patternLineEdit.setText(self.interaction_block.block.title)
        self.ui.blockDescriptionLineEdit.setText(self.interaction_block.block.description)

        # Message
        speech_act = self.interaction_block.speech_act
        self.ui.messageTextEdit.setText(speech_act.message)
        self.ui.messageTypeComboBox.setCurrentIndex(
            self.ui.messageTypeComboBox.findText(speech_act.message_type.name.title(), QtCore.Qt.MatchFixedString))

        # gestures
        self.ui.openGestureLineEdit.setText(
            "{}".format(self.interaction_block.behavioral_parameters.gesture.gestures['open']))
        self.ui.closeGestureLineEdit.setText(
            "{}".format(self.interaction_block.behavioral_parameters.gesture.gestures['close']))
        gestures = config_helper.get_gestures()
        self.ui.openGestureComboBox.clear()
        self.ui.openGestureComboBox.addItems([pconfig.SELECT_OPTION])
        self.ui.openGestureComboBox.addItems(sorted([g for g in gestures['open']]))
        self.ui.openGestureComboBox.currentIndexChanged.connect(lambda: self.update_gesture_text_box(
            combo_box=self.ui.openGestureComboBox,
            text_box=self.ui.openGestureLineEdit,
            gesture_type="open"
        ))
        self.ui.closeGesturesComboBox.clear()
        self.ui.closeGesturesComboBox.addItems([pconfig.SELECT_OPTION])
        self.ui.closeGesturesComboBox.addItems(sorted([g for g in gestures['close']]))
        self.ui.closeGesturesComboBox.currentIndexChanged.connect(lambda: self.update_gesture_text_box(
            combo_box=self.ui.closeGesturesComboBox,
            text_box=self.ui.closeGestureLineEdit,
            gesture_type="close"
        ))

        # tablet page
        # self.ui.tabletPageNameComboBox.clear()
        # self.ui.tabletPageNameComboBox.addItems(pconfig.tablet_pages)
        tablet_page = self.interaction_block.tablet_page
        if not tablet_page.name == "":
            self.ui.tabletPageNameComboBox.setCurrentIndex(
                self.ui.tabletPageNameComboBox.findText(tablet_page.name, QtCore.Qt.MatchFixedString))
        if not tablet_page.image == "":
            self.ui.tabletImageComboBox.setCurrentIndex(
                self.ui.tabletImageComboBox.findText(tablet_page.image, QtCore.Qt.MatchFixedString))
        self.ui.tabletHeadingTextEdit.setText(tablet_page.heading)
        self.ui.tabletInfoTextEdit.setText(tablet_page.text)

        # topic tag
        self.ui.topicNameComboBox.currentIndexChanged.connect(self.update_tags)
        self.ui.topicTagComboBox.currentIndexChanged.connect(self.update_pages)
        self.toggle_topic_tab()

    def toggle_topic_tab(self):
        pattern = "{}".format(self.ui.patternLineEdit.text())
        topic_index = self.ui.tabWidget.indexOf(self.ui.tabWidget.findChild(QtWidgets.QWidget, 'topicTab'))

        if "monologue" in pattern.lower():
            self.ui.tabWidget.setTabEnabled(topic_index, False)  # or use: self.ui.topicTab.setEnabled(False)
            self._set_topic_tab(reset=True)
        else:
            self.ui.tabWidget.setTabEnabled(topic_index, True)  # or use: self.ui.topicTab.setEnabled(True)
            self._set_topic_tab(reset=False)

    def update_tags(self):
        # tags
        self.ui.topicTagComboBox.clear()
        # self.ui.topicTagComboBox.addItems([pconfig.SELECT_OPTION])
        topic_name = "{}".format(self.ui.topicNameComboBox.currentText())
        topics = config_helper.get_topics()
        if topic_name in topics:
            self.ui.topicTagComboBox.addItems([pconfig.SELECT_OPTION])
            self.ui.topicTagComboBox.addItems([tag for tag in topics[topic_name]['tags']])

        self.update_pages()

    def update_pages(self):
        self.ui.tabletPageNameComboBox.clear()
        self.ui.tabletPageNameComboBox.addItems([pconfig.SELECT_OPTION])
        app_props = self.get_app_properties()

        # check topic tag pages
        tag = "{}".format(self.ui.topicTagComboBox.currentText())
        if (pconfig.SELECT_OPTION in tag) or (tag == ""):
            # use default pages
            self.ui.tabletPageNameComboBox.addItems(app_props['tablet']['pages'])
        else:
            self.ui.tabletPageNameComboBox.addItems(
                app_props['topics']["{}".format(self.ui.topicNameComboBox.currentText())]['tags'][tag]['pages'])

    def update_gesture_text_box(self, combo_box, text_box, gesture_type):
        gesture_name = "{}".format(combo_box.currentText())

        if pconfig.SELECT_OPTION in gesture_name:
            return

        gest = config_helper.get_gestures()[gesture_type]
        if gesture_name in gest:
            text_box.setText("{}".format(gest[gesture_name][0]))

    def get_app_properties(self):
        return config_helper.get_app_properties()

    def _set_topic_tab(self, reset=False):
        # set answers and feedbacks
        if reset is True:
            tag, topic, a1, a2, f1, f2 = ('',) * 6
        else:
            topic_tag = self.interaction_block.topic_tag
            tag = topic_tag.name
            topic = topic_tag.topic
            a1 = '' if len(topic_tag.answers) == 0 else topic_tag.answers[0]
            a2 = '' if len(topic_tag.answers) < 2 else topic_tag.answers[1]

            f1 = '' if len(topic_tag.feedbacks) == 0 else topic_tag.feedbacks[0]
            f2 = '' if len(topic_tag.feedbacks) < 2 else topic_tag.feedbacks[1]

        app_props = self.get_app_properties()

        # set topic tab
        self.ui.topicNameComboBox.clear()
        self.ui.topicNameComboBox.addItems([pconfig.SELECT_OPTION])
        available_topics = [t for t in config_helper.get_topics()]
        self.ui.topicNameComboBox.addItems(available_topics)
        if topic.lower() != "":
            self.ui.topicNameComboBox.setCurrentIndex(
                self.ui.topicNameComboBox.findText(topic.lower(), QtCore.Qt.MatchFixedString))
        # tags
        self.update_tags()
        self.ui.topicTagComboBox.setCurrentIndex(
            self.ui.topicTagComboBox.findText(tag.lower(), QtCore.Qt.MatchFixedString))

        self.ui.answer1TextEdit.setText(a1)
        self.ui.answer2TextEdit.setText(a2)
        self.ui.feedback1TextEdit.setText(f1)
        self.ui.feedback2TextEdit.setText(f2)

    def get_speech_act(self):
        return SpeechAct.create_speech_act({"message": "{}".format(self.ui.messageTextEdit.toPlainText()).strip(),
                                            "message_type": "{}".format(self.ui.messageTypeComboBox.currentText())
                                            })

    def get_topic_tag(self):
        if self.ui.topicTab.isEnabled():
            return TopicTag(name="{}".format(self.ui.topicTagComboBox.currentText()),
                            topic="{}".format(self.ui.topicNameComboBox.currentText()),
                            answers=["{}".format(self.ui.answer1TextEdit.toPlainText()).strip(),
                                     "{}".format(self.ui.answer2TextEdit.toPlainText()).strip()],
                            feedbacks=["{}".format(self.ui.feedback1TextEdit.toPlainText()).strip(),
                                       "{}".format(self.ui.feedback2TextEdit.toPlainText()).strip()])
        else:
            return TopicTag()

    def get_tablet_page(self):
        return TabletPage(name="{}".format(self.ui.tabletPageNameComboBox.currentText()),
                          heading="{}".format(self.ui.tabletHeadingTextEdit.toPlainText()).strip(),
                          text="{}".format(self.ui.tabletInfoTextEdit.toPlainText()).strip(),
                          image="{}".format(self.ui.tabletImageComboBox.currentText()),
                          )

    def get_interaction_block(self):
        d_block = self.interaction_block.clone()
        d_block.name = "{}".format(self.ui.patternLineEdit.text().strip())
        d_block.description = "{}".format(self.ui.blockDescriptionLineEdit.text().strip())
        d_block.speech_act = self.get_speech_act()
        d_block.topic_tag = self.get_topic_tag()
        d_block.tablet_page = self.get_tablet_page()
        # gestures
        d_block.behavioral_parameters.gesture.set_gestures(open_gesture="{}".format(self.ui.openGestureLineEdit.text()),
                                                           close_gesture="{}".format(
                                                               self.ui.closeGestureLineEdit.text()))

        return d_block

    def _toggle_item(self, item, status):
        if item is None or status is None:
            return

        try:
            item.setEnabled(status)
            self.repaint()
        except Exception as e:
            self.logger.info("Error while enabling item: {} | {}".format(item, e))
        finally:
            return
