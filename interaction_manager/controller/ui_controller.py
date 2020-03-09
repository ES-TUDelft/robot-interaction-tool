#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# ============= #
# UI_CONTROLLER #
# ============= #
# Class for controlling the main dialog GUI.
#
# @author ES
# **

import logging
import os

from PyQt5 import QtCore, QtGui, QtWidgets

import es_common.hre_config as pconfig
import interaction_manager.utils.json_helper as json_helper
from es_common.enums.led_enums import LedColor
from es_common.enums.speech_enums import *
from es_common.enums.voice_enums import *
from interaction_manager.controller.block_controller import BlockController
from interaction_manager.controller.database_controller import DatabaseController
from interaction_manager.controller.interaction_controller import InteractionController
from interaction_manager.controller.ui_confirmation_dialog_controller import UIConfirmationDialogController
from interaction_manager.controller.ui_edit_block_controller import UIEditBlockController
from interaction_manager.controller.ui_export_blocks_controller import UIExportBlocksController
from interaction_manager.controller.ui_import_blocks_controller import UIImportBlocksController
from interaction_manager.controller.ui_robot_connection_controller import UIRobotConnectionController
from interaction_manager.model.behavioral_parameters import BehavioralParameters
from interaction_manager.model.interaction_design import InteractionDesign
from interaction_manager.view.ui_dialog import Ui_DialogGUI


class UIController(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(UIController, self).__init__(parent)

        self.logger = logging.getLogger("UIController")

        self.robot_controller = None

        self.image_viewer = None
        self.start_time = 0.0
        self.behavioral_parameters = BehavioralParameters()
        self.copied_behavioral_parameters = None
        self.interaction_blocks = []
        self.selected_block = None

        self.interaction_design = None
        self.allow_duplicates = True
        self.volume = pconfig.default_voice_volume
        self.database_controller = None
        self.right_click_menu = None

        self.block_controller = None
        self.interaction_controller = None

        # init UI elements
        self._init_ui()

    def _init_ui(self):
        self.ui = Ui_DialogGUI()
        self.ui.setupUi(self)

        # init controllers
        self._setup_block_controller()
        self.interaction_controller = InteractionController(block_controller=self.block_controller)

        # Attach action listeners
        # CONNECTIONS
        # ===========
        self.ui.actionMenuConnect.triggered.connect(self.robot_connect)
        self.ui.actionMenuDisconnect.triggered.connect(self.robot_disconnect)
        self.ui.actionMenuDatabaseConnect.setEnabled(True)
        self.ui.actionMenuDatabaseConnect.triggered.connect(self.database_connect)
        self.ui.actionMenuDatabaseDisconnect.triggered.connect(self.database_disconnect)
        # ROBOT POSTURE
        # -------------
        self.ui.actionMenuWakeUp.triggered.connect(self.wakeup)
        self.ui.actionMenuRest.triggered.connect(self.rest)
        # TOUCH
        # ------
        self.ui.actionMenuEnableTouch.triggered.connect(self.enable_touch)
        # TABLET
        # ------
        self.ui.actionMenuShowImage.triggered.connect(self.show_image_on_tablet)
        self.ui.actionMenuHideImage.triggered.connect(self.hide_image_on_tablet)
        # SPEECH
        # ------
        self.ui.actionMenuPlay.setEnabled(True)
        self.ui.actionMenuPlay.triggered.connect(self.play_blocks)
        # TODO: check these listeners
        self.ui.actionMenuStop.triggered.connect(self.interaction_controller.stop_engagement_callback)
        self.ui.actionMenuVolumeUp.triggered.connect(self.volume_up)
        self.ui.actionMenuVolumeDown.triggered.connect(self.volume_down)
        # RELOAD
        # ------
        self.ui.actionReload.triggered.connect(self.reset_behavioral_parameters)
        # UNDO/REDO
        # ---------
        self.ui.actionMenuUndo.setEnabled(True)
        self.ui.actionMenuRedo.setEnabled(True)
        self.ui.actionMenuUndo.triggered.connect(self.on_undo)
        self.ui.actionMenuRedo.triggered.connect(self.on_redo)
        # CLEAR/DELETE
        # ============
        self.ui.actionMenuClear.triggered.connect(self.clear_drop_list)

        # COPY/PASTE
        # ----------
        # TODO: Copy block not parameters
        self.ui.actionMenuCopy.triggered.connect(self.copy_behavioral_parameters)
        self.ui.actionMenuPasteSettings.triggered.connect(self.paste_behavioral_parameters)

        # COMMUNICATION & BEHAVIORAL PARAMETERS
        # --------------------------------------
        # group eye color buttons
        self.eye_color_radio_buttons = [self.ui.whiteEyeColorRadioButton, self.ui.redEyeColorRadioButton,
                                        self.ui.greenEyeColorRadioButton, self.ui.blueEyeColorRadioButton]
        self._set_behavioral_parameters_elements()

        # Eye color
        self.ui.whiteEyeColorRadioButton.toggled.connect(lambda: self.eye_color(self.ui.whiteEyeColorRadioButton))
        self.ui.redEyeColorRadioButton.toggled.connect(lambda: self.eye_color(self.ui.redEyeColorRadioButton))
        self.ui.greenEyeColorRadioButton.toggled.connect(lambda: self.eye_color(self.ui.greenEyeColorRadioButton))
        self.ui.blueEyeColorRadioButton.toggled.connect(lambda: self.eye_color(self.ui.blueEyeColorRadioButton))

        # behvioral parameters
        self.ui.gestureOpennessSlider.valueChanged.connect(lambda: self.gesture_openness(self.ui.gestureOpennessSlider))
        self.ui.gazePatternSlider.valueChanged.connect(lambda: self.gaze_pattern(self.ui.gazePatternSlider))
        self.ui.proxemicsSlider.valueChanged.connect(lambda: self.proxemics(self.ui.proxemicsSlider))
        self.ui.voicePitchSlider.valueChanged.connect(lambda: self.voice_pitch(self.ui.voicePitchSlider))
        self.ui.voiceSpeedSlider.valueChanged.connect(lambda: self.voice_speed(self.ui.voiceSpeedSlider))
        self.ui.voiceProsodySlider.valueChanged.connect(lambda: self.voice_prosody(self.ui.voiceProsodySlider))

        # TEST button
        self.ui.testBehavioralParametersButton.clicked.connect(self.test_behavioral_parameters)
        # Apply buttons
        self.ui.behavioralParametersApplyButton.clicked.connect(self.apply_behavioral_parameters)
        self.ui.behavioralParametersApplyToAllButton.clicked.connect(
            lambda: self.apply_behavioral_parameters(to_all_items=True))

        # DELETE, RESET, CLEAR, IMPORT and SAVE list listeners
        self.ui.actionMenuSave.triggered.connect(self.save_drop_list)
        self.ui.actionMenuImportBlocks.triggered.connect(self.import_drop_list)
        self.ui.actionMenuExportBlocks.triggered.connect(self.export_drop_list)

        # CREATE BLOCK
        # -------------
        # TODO: MOVING!!!
        # Enable Moving
        # -------------
        # TODO: replace by action menu
        # self.ui.enableMovingCheckBox.clicked.connect(self.enable_moving)

        # Create dialogue blocks
        # self.create_drag_blocks()
        # self._enable_buttons([self.ui.actionMenuPlay], True)

        # behavioral parameters widget ==> does it need a controller class?
        self.ui.behavioralParametersDockWidget.setFloating(True)
        self.ui.behavioralParametersDockWidget.setHidden(True)

    def _setup_block_controller(self):
        self.block_controller = BlockController(parent_widget=self)

        # remove tmp widget and setup the blocks controller
        self.ui.designPanelLayout.removeWidget(self.ui.tmpWidget)

        # add design widget in the middle
        self.ui.designPanelLayout.addWidget(self.block_controller.get_block_widget())

        # add dock list widget
        self.block_dock_widget = self.block_controller.create_block_dock()
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.block_dock_widget)
        self.tabifyDockWidget(self.ui.blocksDockWidget, self.block_dock_widget)
        self.removeDockWidget(self.ui.blocksDockWidget)

        # observe selected blocks
        self.block_controller.block_is_selected_observable.add_observer(self.block_is_selected)
        self.block_controller.no_block_selected_observable.add_observer(self.no_block_selected)
        self.block_controller.block_settings_observable.add_observer(self.block_settings)
        self.block_controller.block_editing_observable.add_observer(self.block_editing)
        self.block_controller.add_right_click_block_observer(self.create_popup_menu)

    def block_is_selected(self, block):
        self.selected_block = block
        self.update_parameters_widget()

    def no_block_selected(self, event):
        self.selected_block = None
        self._set_warning_label_color(reset=True)

        # Disable behavioral parameters widget
        self._toggle_widget(widget=self.ui.behavioralParametersDockWidget,
                            btns=[],
                            enable=False)

        self.ui.behavioralParametersDockWidget.setHidden(True)

    def block_editing(self, block):
        self.selected_block = block

        # Open edit dialog
        edit_dialog = UIEditBlockController(interaction_block=self.selected_block.parent)

        if edit_dialog.exec_():
            d_block = edit_dialog.get_interaction_block()
            self.selected_block.parent.name = d_block.name
            self.selected_block.parent.description = d_block.description
            self.selected_block.parent.speech_act = d_block.speech_act
            self.selected_block.parent.gestures = d_block.gestures
            self.selected_block.parent.topic_tag = d_block.topic_tag
            self.selected_block.parent.tablet_page = d_block.tablet_page

            self.block_controller.store("Edited block")

        # backup
        self.backup_drop_list()

    def block_settings(self, block):
        # Enable behavioral parameters widget
        self.ui.behavioralParametersDockWidget.setHidden(False)

        self.update_parameters_widget()

    def update_parameters_widget(self):
        if self.selected_block is None:
            return False

        self._set_warning_label_color(reset=True)

        self._toggle_widget(widget=self.ui.behavioralParametersDockWidget,
                            btns=[],
                            enable=True)

        # Set widget's behavioral parameter
        self.ui.behavioral_parameters = self.selected_block.parent.behavioral_parameters.clone()
        self._set_behavioral_parameters_elements(self.ui.behavioral_parameters)

        self.ui.behavioralParametersDockWidget.repaint()

    # ---------- #
    # Connection
    # ---------- #
    def robot_connect(self):
        if self.interaction_controller is None:
            self.interaction_controller = InteractionController()

        connection_dialog = UIRobotConnectionController(self.interaction_controller)

        if connection_dialog.exec_():
            if connection_dialog.success is True:
                self.logger.debug("Robot is_awake = {}".format(connection_dialog.is_awake))
                self._toggle_buttons(is_awake=connection_dialog.is_awake)

                self._enable_buttons([self.ui.actionMenuConnect], enabled=False)
                self._enable_buttons([self.ui.actionMenuDisconnect], enabled=True)
            else:
                self._enable_buttons([self.ui.actionMenuConnect], enabled=True)
                self._enable_buttons([self.ui.actionMenuDisconnect, self.ui.actionMenuWakeUp], enabled=False)
                self._display_message(error="Please enter a valid IP and PORT")
        else:
            self._display_message(error="Connection is canceled!")
            self.robot_disconnect()

        self.repaint()

    def robot_disconnect(self):
        success = self.interaction_controller.disconnect_from_robot()

        # update GUI
        self._toggle_buttons(is_awake=False)
        self._enable_buttons([self.ui.actionMenuConnect], enabled=True)
        self._enable_buttons([self.ui.actionMenuDisconnect, self.ui.actionMenuWakeUp], enabled=False)
        self._display_message(message="### Disconnected from the robot.")

        self.repaint()

    # --------- #
    # MONGO DB
    # --------- #
    def database_connect(self):
        self.database_controller = DatabaseController()

        message, error = self.database_controller.connect()

        if error is None:
            self._display_message(message=message)
            self._enable_buttons([self.ui.actionMenuDatabaseDisconnect, self.ui.actionMenuSave, self.ui.saveDropListButton],
                                 enabled=True)
            self._enable_buttons([self.ui.actionMenuDatabaseConnect], enabled=False)
        else:
            self._display_message(error=error)

        self.repaint()

    def database_disconnect(self):
        if self.database_controller is None:
            self._display_message(message='Database was already disconnected')
        else:
            message, error = self.database_controller.disconnect()
            if error is None:
                self._display_message(message=message)
            else:
                self._display_message(error=error)

        self._enable_buttons([self.ui.actionMenuDatabaseDisconnect, self.ui.actionMenuSave, self.ui.saveDropListButton],
                             enabled=False)
        self._enable_buttons([self.ui.actionMenuDatabaseConnect], enabled=True)

        self.repaint()

    # ----------- #
    # Robot Start
    # ----------- #
    def wakeup(self):
        success = self.interaction_controller.wakeup_robot()
        self._toggle_buttons(is_awake=success)
        self._display_message(message="Pepper is awake and ready for action.")
        self.repaint()

    def rest(self):
        self.interaction_controller.rest_robot()
        self._toggle_buttons(is_awake=False)
        self._display_message(message="Pepper is Resting")
        self.repaint()

    # TOUCH
    # ------
    def enable_touch(self):
        self.interaction_controller.enable_touch()
        self._enable_buttons([self.ui.actionMenuEnableTouch], False)
        self.repaint()

    # TRACKING
    # ---------
    def tracking(self, enable=True):
        self.interaction_controller.tracking(enable=enable)

    def test_behavioral_parameters(self):
        message, error = self.interaction_controller.test_behavioral_parameters(self.selected_block.parent,
                                                                                self.behavioral_parameters.clone(),
                                                                                self.volume)
        self._display_message(message=message, error=error)

    def volume_up(self):
        vol = self.volume + pconfig.volume_increase
        self.set_volume(vol)
        self._display_message("Volume set to: {}".format(self.volume))

    def volume_down(self):
        vol = self.volume - pconfig.volume_increase
        self.set_volume(vol)
        self._display_message("Volume set to: {}".format(self.volume))

    def set_volume(self, vol=pconfig.default_voice_volume):
        if self._check_value(vol, pconfig.voice_volume_range[0], pconfig.voice_volume_range[1]) is True:
            self.volume = vol

    # TABLET
    # ------
    def show_image_on_tablet(self):
        self.interaction_controller.tablet_image(hide=False)
        self._enable_buttons([self.ui.actionMenuShowImage], enabled=False)
        self._enable_buttons([self.ui.actionMenuHideImage], enabled=True)
        self.repaint()

    def hide_image_on_tablet(self):
        self.interaction_controller.tablet_image(hide=True)
        self._enable_buttons([self.ui.actionMenuShowImage], enabled=True)
        self._enable_buttons([self.ui.actionMenuHideImage], enabled=False)
        self.repaint()

    # MOVEMENT
    # --------
    def enable_moving(self):
        self.interaction_controller.enable_moving()

    def play_blocks(self):
        # check if the scene contains a valid start block
        # if yes, send the request to the interaction controller
        block = self.block_controller.has_block(pattern="start")
        if block is None:
            self._display_message(error="The scene doesn't contain a starting block! "
                                        "Please add a 'START' block then click on play")
        else:
            self._display_message(message="Attempting to play the interaction!")
            self.interaction_controller.start_playing(int_block=block.parent)

        # TODO: call interaction_controller
        # self.interaction_controller.play_blocks(...)
        # if len(self.interaction_blocks) > 0:
        #    self._enable_buttons([self.ui.actionMenuPlay], enabled=False)
        #    self._enable_buttons([self.ui.actionMenuStop], enabled=True)

    # BEHAVIORAL PARAMETERS
    # ---------------------
    # Can be used to simplify the remaining functions!
    def slider_listener(self, slider, the_enum, beh_param_property):
        val = slider.value() if slider.value() in the_enum.values() else 0
        beh_param_property = the_enum(val)

    def gesture_openness(self, slider):
        val = slider.value() if slider.value() in GesturesType.values() else 0
        self.behavioral_parameters.gestures_type = GesturesType(val)
        self._set_warning_label_color(c=pconfig.warning_color_rgb)

    def gaze_pattern(self, slider):
        val = slider.value() if slider.value() in GazePattern.values() else 0
        self.behavioral_parameters.gaze_pattern = GazePattern(val)
        self._set_warning_label_color(c=pconfig.warning_color_rgb)

    def voice_prosody(self, slider):
        val = slider.value() if slider.value() in VoiceProsody.values() else 0
        self.behavioral_parameters.voice.prosody = VoiceProsody(val)
        self._set_warning_label_color(c=pconfig.warning_color_rgb)

    def voice_pitch(self, slider):
        self.behavioral_parameters.voice.pitch = (float(slider.value()) * 0.1) + 1
        self._set_warning_label_color(c=pconfig.warning_color_rgb)

    def voice_speed(self, slider):
        self.behavioral_parameters.voice.speed = (float(slider.value()) * 10) + 100
        self._set_warning_label_color(c=pconfig.warning_color_rgb)

    def proxemics(self, slider):
        p_val = self._convert_proxemics(value=float(slider.value()), to_float=True)
        self.ui.proxemicsLcdNumber.display(p_val)
        self.behavioral_parameters.proxemics = p_val
        self._set_warning_label_color(c=pconfig.warning_color_rgb)

    def eye_color(self, btn):
        self.behavioral_parameters.eye_color = LedColor[btn.text().upper()]
        self._set_warning_label_color(c=pconfig.warning_color_rgb)

    def apply_behavioral_parameters(self, to_all_items=False):
        if to_all_items is True:
            confirmation_dialog = UIConfirmationDialogController(message="The changes will be applied to all items.")
            if confirmation_dialog.exec_():
                self.block_controller.update_blocks_behavioral_parameters(
                    param_name="{}".format(self.ui.behavioralParametersApplyComboBox.currentText()),
                    behavioral_parameters=self.behavioral_parameters)

                self._display_message(message="The parameters of all blocks are updated.")
        else:
            if self.selected_block is not None:
                self.selected_block.parent.behavioral_parameters = self.behavioral_parameters.clone()

                self._display_message(message="The '{}' parameters are updated.".format(self.selected_block.title))
                self.block_controller.store("Updated parameters for {}".format(self.selected_block.title))

        # backup
        self.backup_drop_list()
        # reset warning
        self._set_warning_label_color(reset=True)

        self.ui.behavioralParametersDockWidget.repaint()
        self.ui.logsDockWidget.repaint()

    def reset_behavioral_parameters(self):
        self.behavioral_parameters = BehavioralParameters()
        # self.logger.info("*** {}".format(self.behavioral_parameters.voice.to_dict))
        self._set_behavioral_parameters_elements()
        self._display_message(message="Behavioral parameters successfully reset.")
        self.ui.behavioralParametersDockWidget.repaint()
        self.ui.logsDockWidget.repaint()

    def copy_behavioral_parameters(self):
        self.copied_behavioral_parameters = self.behavioral_parameters.clone()
        self._enable_buttons(buttons=[self.ui.actionMenuPasteSettings], enabled=True)

    def paste_behavioral_parameters(self):
        if self.selected_block is not None:
            self.selected_block.parent.set_behavioral_parameters(
                p_name="{}".format(self.ui.behavioralParametersApplyComboBox.currentText()),
                behavioral_parameters=self.copied_behavioral_parameters)

            # backup
            self.backup_drop_list()

            self.behavioral_parameters = self.selected_block.parent.behavioral_parameters.clone()
            self._set_behavioral_parameters_elements(self.behavioral_parameters)

            self._display_message(message="Successfully pasted the parameters.")

            self.ui.behavioralParametersDockWidget.repaint()

    #
    # MENU ACTIONS
    #
    def on_file_new(self):
        self.block_controller.clear_scene()

    def on_undo(self):
        self.block_controller.undo()
        self.no_block_selected(None)
        # self.repaint()

    def on_redo(self):
        self.block_controller.redo()
        self.no_block_selected(None)
        # self.repaint()

    # -------------------- #
    # Interaction Block Lists
    # -------------------- #
    def create_popup_menu(self, event):
        """
        Creates a popup menu when the user right-clicks on a block
        """
        self.right_click_menu = QtWidgets.QMenu(self)

        item = self.block_controller.get_item_at(event.pos())

        if hasattr(item, "block"):
            self.logger.debug("item has block attribute: {}".format(item))
            block = item.block

            # enable widget
            # TODO: enable right click menu

            # Add an edit block action
            self.right_click_menu.addAction("Edit")

            # Add a separator
            self.right_click_menu.addSeparator()

            # Add an edit block action
            self.right_click_menu.addAction("Set Parameters")

            # Add a separator
            self.right_click_menu.addSeparator()

            # Add copy/paste settings action
            self.right_click_menu.addAction("Copy Settings")
            self.right_click_menu.addAction("Paste Settings")

            # Add a separator
            self.right_click_menu.addSeparator()

            # Add a delete block action
            self.right_click_menu.addAction("Delete")

            # Add a separator
            self.right_click_menu.addSeparator()

            # Add a duplicate option
            self.right_click_menu.addAction("Duplicate")

            # TODO:
            action = self.right_click_menu.exec_(self.block_controller.get_block_widget().mapToGlobal(event.pos())) #self.block_controller.get_block_widget(), event.pos()))
            if action:
                self.execute_right_click_action(action, block)

    def execute_right_click_action(self, action, block):
        """
        Function that executes popup menu actions
        """
        action_name = str(action.text()).translate(None, '&')
        if action_name == "Delete":
            # TODO: delete block
            pass
        elif action_name == "Edit":
            self.block_editing(block)
        elif action_name == "Set Parameters":
            self.block_settings(block)
        elif action_name == "Copy Settings":
            self.copy_behavioral_parameters()
        elif action_name == "Paste Settings":
            self.paste_behavioral_parameters()
        elif action_name == "Duplicate":
            pass  # self.duplicate_block()

    def duplicate_block(self):
        # TODO: implement duplicating a block
        # backup
        self.backup_drop_list()

        self._display_message(message="Successfully duplicated the block.")
        self.ui.behavioralParametersDockWidget.repaint()
        self.repaint()

    def _fill_widget_with_blocks(self, blocks=[]):
        # TODO: fill scene with imported blocks
        self.block_controller.clear_scene()

        # self.block_controller.clear_selection()

    def clear_drop_list(self):
        # Ask for confirmation
        confirmation_dialog = UIConfirmationDialogController(message="All blocks will be deleted!")
        if confirmation_dialog.exec_():
            self.block_controller.clear_scene()

            # Disable widget
            self._toggle_widget(widget=self.ui.behavioralParametersDockWidget,
                                btns=[], enable=False)
            # backup
            self.backup_drop_list()

            self.repaint()

    def delete_drop_list_items(self):
        # TODO: delete selected blocks

        # Disable widget
        self._toggle_widget(widget=self.ui.behavioralParametersDockWidget,
                            btns=[], enable=False)
        # backup
        self.backup_drop_list()
        self.repaint()

    def create_interaction_design(self):
        return InteractionDesign(communication_style="Interaction")

    def insert_interaction_design(self, design):
        success = self.database_controller.insert_interaction_design(design=design)

        self._display_message(message="Successfully inserted the selected interaction blocks.") if success is True else \
            self._display_message(error="Error while inserting interaction blocks.")

    def export_drop_list(self):
        # TODO: get dict of blocks
        interaction_design = self.create_interaction_design()
        interaction_design.blocks = {}

        # open export dialog
        export_dialog = UIExportBlocksController(interaction_design=interaction_design)
        if export_dialog.exec_():
            self._display_message(message="Successfully exported the interaction blocks.")

    def backup_drop_list(self):
        # TODO: backup!
        interaction_design = self.create_interaction_design()
        interaction_design.blocks = {}

        foldername = "{}/logs".format(os.getcwd())
        _, error = json_helper.export_blocks(filename=interaction_design.communication_style,
                                             foldername=foldername, interaction_design=interaction_design)
        if error is not None:
            self._display_message(error=error)

    def save_drop_list(self):
        # TODO: save list
        self._display_message(error="Save method is not implemented!")
        # interaction_design = self.create_interaction_design()
        # interaction_design.blocks = {}  # self.ui.dropListWidget.to_dict

        # self.insert_interaction_design(interaction_design)

    def import_drop_list(self):
        # TODO: import blocks
        # open import dialog
        import_dialog = UIImportBlocksController()

        if import_dialog.exec_():
            if import_dialog.blocks is None or len(import_dialog.blocks) == 0: return
            # TODO: fill scene with blocks
            # self._fill_widget_with_blocks(self.ui.dropListWidget, import_dialog.blocks)

            # Disable behavioral parameters widget
            self._toggle_widget(widget=self.ui.behavioralParametersDockWidget,
                                btns=[], enable=False)
            # backup
            self.backup_drop_list()
            self._display_message(message="New blocks are imported.")
            self.repaint()

    def _check_value(self, value, start, stop):
        if start <= value <= (stop + 1):
            return True
        else:
            self.logger.error("*** Please provide a value in range: [{}, {}]".format(start, stop))
            return False

    def _set_behavioral_parameters_elements(self, behavioral_parameters=None):
        if behavioral_parameters is None:
            behavioral_parameters = self.behavioral_parameters
        self.ui.gestureOpennessSlider.setValue(behavioral_parameters.gestures_type.value)
        self.ui.gazePatternSlider.setValue(behavioral_parameters.gaze_pattern.value)
        # roll back the proxemics value
        self.ui.proxemicsSlider.setValue(self._convert_proxemics(value=behavioral_parameters.proxemics, to_int=True))
        self.ui.proxemicsLcdNumber.display(behavioral_parameters.proxemics)
        self.ui.voicePitchSlider.setValue(int(round((behavioral_parameters.voice.pitch - 1) / .1, 1)))
        self.ui.voiceSpeedSlider.setValue(int((behavioral_parameters.voice.speed - 100) / 10))
        self.ui.voiceProsodySlider.setValue(behavioral_parameters.voice.prosody.value)
        self._check_eye_color_btn(color=behavioral_parameters.eye_color)

        # reset warning label
        self._set_warning_label_color(reset=True)
        self.repaint()

    def _set_warning_label_color(self, c=None, reset=False):
        if c is None or c == "" or reset is True:
            c = pconfig.default_color_rgb
        self.ui.warningLabel.setStyleSheet("QLabel { color : " + c + "; }")

    def _convert_proxemics(self, value=0.0, to_int=False, to_float=False):
        if to_int is True:
            return int((value - pconfig.proxemics_initial_value) / pconfig.proxemics_multiplier)
        elif to_float is True:
            return float(value * pconfig.proxemics_multiplier) + pconfig.proxemics_initial_value
        else:
            return 1

    def _check_eye_color_btn(self, color=LedColor.WHITE):
        for btn in self.eye_color_radio_buttons:
            if btn.text().lower() == color.name.lower():
                self._check_buttons([btn], checked=True)
                return

    def _set_combo_box(self, combo_box, items):
        combo_box.clear()
        combo_box.addItems(items)

    def _connect_radio_button_listeners(self, func=None, btns=[]):
        if func is None: return

        for btn in btns:
            btn.toggled.connect(lambda: func(btn))

    def _connect_slider_listeners(self, func=None, sliders=[], enums=[]):
        if func is None: return

        for i in range(0, len(sliders)):
            sliders[i].valueChanged.connect(lambda: func(sliders[i], enums[i]))

    def _get_index_of_current_item(self):
        # TODO: index of selected item
        indexes = None
        if indexes:
            return indexes[0].row()
        return -1

    def _display_message(self, message=None, error=None):
        if message is None:
            self.ui.logsTextEdit.setTextColor(QtGui.QColor('red'))  # red text for errors
            self.ui.logsTextEdit.append(error)
            self.logger.error(error)
        else:
            self.ui.logsTextEdit.setTextColor(QtGui.QColor('white'))  # white text for normal
            self.ui.logsTextEdit.append(message)
            self.logger.info(message)
        self.repaint()

    def _enable_buttons(self, buttons=[], enabled=False):
        for button in buttons:
            try:
                button.setEnabled(enabled)
                button.setChecked(False)
            except Exception as e:
                self.logger.info("Error while enabling button: {} | {}".format(button, e))
            finally:
                pass

    def _check_buttons(self, btns=[], checked=False):
        if btns is None: return

        for btn in btns:
            btn.setChecked(checked)
            try:
                btn.setChecked(checked)
            except Exception as e:
                self.logger.info("Error while checking radio button: {} | {}".format(btn, e))
            finally:
                pass

    def _toggle_widget(self, widget, btns=[], enable=True):
        widget.setEnabled(enable)
        self._enable_buttons(buttons=btns, enabled=enable)

    def _toggle_buttons(self, is_awake=False):
        if is_awake is True:
            # Enable/disable buttons
            self._enable_buttons([self.ui.actionMenuRest, self.ui.actionMenuShowImage,
                                  self.ui.actionMenuEnableTouch,
                                  self.ui.actionMenuVolumeDown, self.ui.actionMenuVolumeUp, self.ui.actionMenuPlay,
                                  self.ui.testBehavioralParametersButton
                                  ], enabled=True)
            self._enable_buttons([self.ui.actionMenuWakeUp, self.ui.actionMenuHideImage,
                                  self.ui.actionMenuStop], enabled=False)
        else:
            # Enable wake up button
            self._enable_buttons([self.ui.actionMenuWakeUp], enabled=True)
            # disable everything
            self._enable_buttons([self.ui.actionMenuRest, self.ui.actionMenuShowImage, self.ui.actionMenuHideImage,
                                  self.ui.actionMenuEnableTouch,
                                  self.ui.actionMenuVolumeDown, self.ui.actionMenuVolumeUp, self.ui.actionMenuPlay,
                                  self.ui.actionMenuStop,
                                  self.ui.testBehavioralParametersButton
                                  ], enabled=False)
