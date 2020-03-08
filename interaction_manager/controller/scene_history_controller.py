#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# ======================== #
# SCENE_HISTORY_CONTROLLER #
# ======================== #
# Class for controlling the scene's history (to allow undo/redo operations).
#
# @author ES
# **

from interaction_manager.controller.history_controller import HistoryController
from interaction_manager.view.graphics_edge import ESGraphicsEdge


class SceneHistoryController(HistoryController):
    def __init__(self, scene):
        super(SceneHistoryController, self).__init__()

        self.scene = scene

    def create_stamp(self, description):
        selected_obj = {
            "blocks": [],
            "edges": []
        }
        for item in self.scene.graphics_scene.selectedItems():
            if hasattr(item, 'block'):
                selected_obj["blocks"].append(item.block.id)
            elif isinstance(item, ESGraphicsEdge):
                selected_obj["edges"].append(item.edge.id)

        stamp = {
            "description": description,
            "snapshot": self.scene.serialize(),
            "selection": selected_obj
        }

        return stamp

    def restore_stamp(self, stamp):
        try:
            self.scene.clear()

            self.scene.deserialize(stamp["snapshot"])
            self.scene.clear_selection()

            # selection ==> not needed
            # for edge_id in stamp["selection"]["edges"]:
            #     for edge in self.scene.edges:
            #         if edge.id == edge_id:
            #             edge.graphics_edge.setSelected(True)
            #             break  # no need to go through all edges
            #
            # for block_id in stamp["selection"]["blocks"]:
            #     for block in self.scene.blocks:
            #         if block.id == block_id:
            #             block.graphics_block.setSelected(True)
            #             break

        except Exception as e:
            self.logger.error("Error while restoring history! {}".format(e))

