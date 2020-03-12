#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# ==================== #
# BLOCK_CONTROLLER #
# ==================== #
# Class for controlling the interactions blocks.
#
# @author ES
# **

import logging

from PyQt5 import QtWidgets, QtCore, QtGui

from es_common.model.observable import Observable
from es_common.utils import block_helper
from interaction_manager.controller.block_list_controller import BlockListWidget
from interaction_manager.enums.block_enums import EdgeType
from interaction_manager.factory.block_factory import BlockFactory
from interaction_manager.model.block import Block
from interaction_manager.model.interaction_block import InteractionBlock
from interaction_manager.utils import config_helper


class BlockController(object):
    def __init__(self, parent_widget=None):
        self.logger = logging.getLogger("AppBlock Controller")

        self.scene = BlockFactory.create_scene()
        self._block_widget = BlockFactory.create_block_widget(scene=self.scene, parent=parent_widget)
        self._block_list_widget = BlockListWidget()

        self.block_is_selected_observable = Observable()
        self.no_block_selected_observable = Observable()
        self.block_settings_observable = Observable()
        self.block_editing_observable = Observable()

        # add observers
        self.add_drag_enter_observer(self.on_drag_enter)
        self.add_drop_observer(self.on_drop)
        self.add_no_block_selected_observer(self.no_block_selected)

        # observe when new blocks are created from undo/redo operations
        block_helper.block_observable.add_observer(self.update_block_selected_observer)

        # store initial state
        self.store("Initial Scene")

    def create_block_dock(self, floating=False):
        blocks_dock = QtWidgets.QDockWidget("Blocks")
        blocks_dock.setWidget(self.get_block_list_widget())
        blocks_dock.setFloating(floating)

        return blocks_dock

    def on_drag_enter(self, event):
        self.logger.debug("Drag entered: {}".format(event.mimeData().text()))
        if event.mimeData().hasFormat(config_helper.get_block_mimetype()):
            # accept drop
            event.acceptProposedAction()
        else:
            # deny drop
            event.setAccepted(False)

    def on_drop(self, event):
        # self.logger.debug("Drop event: {}".format(event.mimeData().text()))
        if event.mimeData().hasFormat(config_helper.get_block_mimetype()):
            event_data = event.mimeData().data(config_helper.get_block_mimetype())
            data_stream = QtCore.QDataStream(event_data, QtCore.QIODevice.ReadOnly)

            item_pixmap = QtGui.QPixmap()
            data_stream >> item_pixmap
            op_code = data_stream.readInt()
            item_text = data_stream.readQString()

            mouse_position = event.pos()
            scene_position = self.get_scene_position(mouse_position)

            self.logger.debug("Item with: {} | {} | mouse: {} | scene pos: {}".format(op_code, item_text,
                                                                                      mouse_position, scene_position))
            # new interaction block
            self.create_interaction_block(title=item_text,
                                          pos=[scene_position.x(), scene_position.y()],
                                          pattern=item_text.lower())
            # self.add_block(title=item_text, num_inputs=2, num_outputs=1,
            #                                pos=[scene_position.x(), scene_position.y()],
            #                                observer=self.block_is_selected)
            self.store("Added new {}".format(item_text))

            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            self.logger.debug("*** drop ignored")
            event.ignore()

    def create_interaction_block(self, title, pos, pattern):
        num_inputs, num_outputs = 0, 1
        icon = None

        patterns = config_helper.get_patterns()
        if pattern is not None and pattern.lower() in patterns:
            num_inputs = patterns[pattern.lower()]["inputs"]
            num_outputs = patterns[pattern.lower()]["outputs"]
            icon = patterns[pattern.lower()]["icon"]
        else:
            pattern = "start"

        # TODO: create block from pattern
        interaction_block = InteractionBlock(name=title, pattern=pattern)
        interaction_block.block = self.add_block(title=title,
                                                 num_inputs=num_inputs, num_outputs=num_outputs,
                                                 pos=pos,
                                                 observer=self.block_is_selected,
                                                 parent=interaction_block,
                                                 icon=icon)
        # editing/settings observers
        interaction_block.block.settings_observables.add_observer(self.block_settings_selected)
        interaction_block.block.editing_observables.add_observer(self.block_editing_selected)

        return interaction_block

    def update_block_selected_observer(self, block):
        if type(block) is Block:
            self.logger.debug("Observer for {} is updated.".format(block.title))
            block.add_observer(self.block_is_selected)
            block.settings_observables.add_observer(self.block_settings_selected)
            block.editing_observables.add_observer(self.block_editing_selected)

    def update_all_blocks_selected_observer(self):
        for block in self.get_blocks():
            self.logger.debug("Observer for {} is updated.".format(block.title))
            block.add_observer(self.block_is_selected)
            # editing/settings observers
            block.settings_observables.add_observer(self.block_settings_selected)
            block.editing_observables.add_observer(self.block_editing_selected)

    def update_blocks_behavioral_parameters(self, param_name, behavioral_parameters):
        # apply settings to all blocks
        for b in self.get_blocks():
            if type(b.parent) is InteractionBlock:  # to be on the safe side!
                b.parent.set_behavioral_parameters(
                    p_name=param_name,
                    behavioral_parameters=behavioral_parameters
                )
        self.store("Updated behavioral parameters of all blocks")

    def block_is_selected(self, block):
        if type(block) is Block:
            self.logger.debug("Block '{}' is selected. | id = {}".format(block.title, block.id))
            self.block_is_selected_observable.notify_all(block)

    def no_block_selected(self, event):
        item = self.get_item_at(event.pos())
        self.logger.debug("No block is selected | {}".format(item))

        self.no_block_selected_observable.notify_all(event)

    def block_settings_selected(self, block):
        if type(block) is Block:
            self.logger.debug("Settings icon of Block '{}' is selected. | id = {}".format(block.title, block.id))
            self.block_settings_observable.notify_all(block)

    def block_editing_selected(self, block):
        if type(block) is Block:
            self.logger.debug("Editing icon of Block '{}' is selected. | id = {}".format(block.title, block.id))
            self.block_editing_observable.notify_all(block)

    def has_block(self, pattern="start"):
        for block in self.get_blocks():
            if block.title.lower() == pattern.lower():
                return block
        return None

    def get_block_widget(self):
        return self._block_widget

    def get_block_list_widget(self):
        return self._block_list_widget

    def add_block(self, title, num_inputs, num_outputs, pos, observer=None, parent=None, icon=None):
        return BlockFactory.create_block(self.scene, title, num_inputs, num_outputs, pos, observer, parent, icon)

    def delete_block(self, block):
        block.remove()
        self.logger.debug("Removed block")

    def add_edge(self, start_socket, end_socket, edge_type=EdgeType.BEZIER):
        return BlockFactory.create_edge(self.scene, start_socket, end_socket, edge_type)

    def delete_edge(self, edge):
        edge.remove()
        self.logger.debug("Removed edge")

    def store(self, description):
        self.scene.history.store(description=description)

    def save_blocks(self, filename):
        self.scene.save_scene(filename=filename)

    def load_blocks(self, filename):
        self.scene.load_scene(filename=filename)

    def load_blocks_data(self, data):
        self.scene.load_scene_data(data=data)

    def get_serialized_scene(self):
        return self.scene.serialize()

    def get_scene_position(self, mouse_position):
        return self._block_widget.get_scene_position(mouse_position)

    def get_item_at(self, pos):
        return self._block_widget.get_item_at(pos)

    def get_blocks(self):
        return self.scene.blocks

    def get_parent_blocks(self):
        blocks = self.scene.blocks

        return None if blocks is None else [b.parent for b in blocks]

    def get_edges(self):
        return self.scene.edges

    def clear_scene(self):
        self.scene.clear()
        self.store("Cleared scene.")

    def clear_selection(self):
        self.scene.clear_selection()

    def undo(self):
        self.scene.history.undo()

    def redo(self):
        self.scene.history.redo()

    def get_block_by_id(self, block_id=0):
        blocks = self.get_blocks()
        if blocks is None:
            return None

        for b in blocks:
            if b.id == block_id:
                return b
        return None

    def get_block_by_parent_id(self, parent_id=0):
        parent_blocks = self.get_parent_blocks()
        if parent_blocks is None:
            return None

        for p in parent_blocks:
            if p.id == parent_id:
                return p
        return None

    ###
    # DRAG and DROP OBSERVERS
    ###
    def add_drag_enter_observer(self, observer):
        self._block_widget.add_drag_enter_observer(observer)

    def remove_drag_enter_observer(self, observer):
        return self._block_widget.remove_drag_enter_observer(observer)

    def add_drop_observer(self, observer):
        self._block_widget.add_drop_observer(observer)

    def remove_drop_observer(self, observer):
        return self._block_widget.remove_drop_observer(observer)

    # BLOCK OBSERVERS
    # ===============
    def add_no_block_selected_observer(self, observer):
        self._block_widget.add_no_block_selected_observer(observer)

    def remove_no_block_selected_observer(self, observer):
        self._block_widget.remove_no_block_selected_observer(observer)

    def add_right_click_block_observer(self, observer):
        self._block_widget.right_click_block_observable.add_observer(observer)

    def add_remove_click_block_observer(self, observer):
        self._block_widget.right_click_block_observable.remove_observer(observer)
