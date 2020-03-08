from collections import OrderedDict
import logging

from interaction_manager.model.edge import Edge
from interaction_manager.model.block import Block
from interaction_manager.view.graphics_scene import ESGraphicsScene
from es_common.datasource.serializable import Serializable
from interaction_manager.utils import data_helper
from interaction_manager.controller.scene_history_controller import SceneHistoryController


class Scene(Serializable):
    def __init__(self):
        super(Scene, self).__init__()

        self.logger = logging.getLogger("Scene")

        self.blocks = []
        self.edges = []

        self.graphics_scene = ESGraphicsScene(self)

        self.history = SceneHistoryController(self)

    def set_scene_rect(self, width, height):
        self.graphics_scene.set_scene_rect(width, height)

    def clear_selection(self):
        self.graphics_scene.clearSelection()

    def add_block(self, block):
        self.blocks.append(block)
        self.graphics_scene.addItem(block.graphics_block)
        self.logger.debug("Added block '{}': {}".format(block.title, block))

    def remove_block(self, block):
        self.graphics_scene.removeItem(block.graphics_block)
        self.blocks.remove(block)
        self.logger.debug("Removed block '{}: {}".format(block.title, block))

    # Edges
    def add_edge(self, edge):
        self.edges.append(edge)
        self.graphics_scene.addItem(edge.graphics_edge)
        self.logger.debug("Added edge to scene '{}: {} | {}".format(edge, edge.start_socket, edge.end_socket))

    def remove_edge(self, edge):
        self.edges.remove(edge)
        self.graphics_scene.removeItem(edge.graphics_edge)
        self.logger.debug("Removed edge from scene '{}: {} | {}".format(edge, edge.start_socket, edge.end_socket))

    def save_scene(self, filename):
        data_helper.save_to_file(filename, self.serialize())

    def load_scene(self, filename):
        scene_data = data_helper.load_data_from_file(filename)
        return self.deserialize(scene_data)

    def clear(self):
        for edge in self.edges:
            edge.remove()
            edge = None
        for block in self.blocks:
            block.remove()
            block = None

        self.graphics_scene.clear()

        self.edges = []
        self.blocks = []

    ###
    # SERIALIZATION
    ###
    def serialize(self):
        return OrderedDict([
            ("id", self.id),
            ("blocks", [b.serialize() for b in self.blocks]),
            ("edges", [e.serialize() for e in self.edges])
        ])

    def deserialize(self, data, hashmap={}):
        # clear scene
        self.clear()

        hashmap = {}

        # create block
        for b_data in data["blocks"]:
            Block(self).deserialize(b_data, hashmap)

        # create edges
        for e_data in data["edges"]:
            Edge(scene=self,
                 start_socket=hashmap[e_data["start_socket"]],
                 end_socket=hashmap[e_data["end_socket"]]
                 ).deserialize(e_data, hashmap)

        return True
