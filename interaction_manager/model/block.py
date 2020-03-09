from collections import OrderedDict

from es_common.model.observable import Observable
from es_common.datasource.serializable import Serializable
from interaction_manager.view.graphics_block import ESGraphicsBlock
from interaction_manager.view.block_content_widget import ESBlockContentWidget
from interaction_manager.model.socket import Socket
from interaction_manager.enums.block_enums import Position, SocketType
import logging

from es_common.utils import block_helper


class Block(Serializable, Observable):

    def __init__(self, scene, title="Start", socket_types=[], pos=[], parent=None, icon=None):
        super(Block, self).__init__()
        Observable.__init__(self)  # explicit call to second parent class

        self.logger = logging.getLogger("Block")

        self.scene = scene
        self.parent = parent  # any container
        self.graphics_block = None

        self.icon = icon
        self.title = title

        self.inputs = []
        self.outputs = []

        self.socket_spacing = 22

        self._init_ui(socket_types, pos)

        # add observables
        self.editing_observables = Observable()
        self.settings_observables = Observable()

        # add editing/settings listeners
        self.content.editing_icon.clicked.connect(lambda: self.editing_observables.notify_all(event=self))
        self.content.settings_icon.clicked.connect(lambda: self.settings_observables.notify_all(event=self))

        # add block to the scene
        self.scene.add_block(self)

    def _init_ui(self, socket_types, pos):
        self.content = ESBlockContentWidget(block=self)
        self.graphics_block = ESGraphicsBlock(block=self)

        self._init_sockets(socket_types)

        if pos is not None and len(pos) == 2:
            self.set_pos(*pos)

    def _init_sockets(self, socket_types):
        in_counter = 0
        out_counter = 0
        for st in socket_types:
            if st is SocketType.INPUT:
                self.inputs.append(Socket(block=self,
                                          index=in_counter,
                                          position=Position.BOTTOM_LEFT,
                                          socket_type=SocketType.INPUT))
                in_counter += 1
            else:
                self.outputs.append(Socket(block=self,
                                           index=out_counter,
                                           position=Position.TOP_RIGHT,
                                           socket_type=SocketType.OUTPUT))
                out_counter += 1

    def get_socket_position(self, index, position):
        # set x
        x = 0  # for the left side
        if position in (Position.TOP_RIGHT, Position.BOTTOM_RIGHT, Position.CENTER_RIGHT):
            x = self.graphics_block.width

        # set y
        if position in (Position.CENTER_LEFT, Position.CENTER_RIGHT):
            y = (self.graphics_block.height / 2) - index * self.socket_spacing
        elif position in (Position.BOTTOM_LEFT, Position.BOTTOM_RIGHT):
            # start on bottom
            y = self.graphics_block.height - (2 * self.graphics_block.rounded_edge_size) - index * self.socket_spacing
        else:
            y = self.graphics_block.title_height + self.graphics_block.rounded_edge_size + index * self.socket_spacing

        return [x, y]

    def update_connected_edges(self):
        for socket in self.inputs + self.outputs:
            socket.update_edge_positions()

    def is_connected_to(self, other_block):
        """
        :param other_block:
        :return: True if two blocks are connected; False otherwise.
        """
        for edge in self.scene.edges:
            if self in (edge.start_socket.block, edge.end_socket.block) and \
                    other_block in (edge.start_socket.block, edge.end_socket.block):
                self.logger.info("{} is connected to {}".format(self, other_block))
                return True

        return False

    def get_connected_blocks(self):
        blocks = []
        if len(self.outputs) > 0:
            # for now, assume we have one output socket
            for socket in self.outputs[0].get_connected_sockets():
                blocks.append(socket.block)

        return blocks

    def remove(self):
        # remove socket edges
        for socket in (self.inputs + self.outputs):
            # remove edges, if any
            socket.disconnect_all_edges()

        # remove block from scene
        self.scene.remove_block(self)
        self.graphics_block = None

    def __str__(self):
        return "<Block id {}..{}>".format((hex(id(self))[2:5]), (hex(id(self))[-3:]))

    def get_pos(self):
        return self.graphics_block.pos()  # QPointF

    def set_pos(self, x, y):
        self.graphics_block.setPos(x, y)

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value
        if self.graphics_block is not None:
            self.graphics_block.title = self.title

    @property
    def icon(self):
        return self.__icon

    @icon.setter
    def icon(self, value):
        self.__icon = value
        if self.graphics_block is not None:
            self.graphics_block.set_title_pixmap(self.icon)

    @property
    def description(self):
        return self.content.description

    @description.setter
    def description(self, desc):
        self.content.description = desc

    ###
    # SERIALIZATION
    ###
    def serialize(self):
        return OrderedDict([
            ("id", self.id),
            ("title", self.title),
            ("icon", self.icon),
            ("pos_x", self.graphics_block.scenePos().x()),
            ("pos_y", self.graphics_block.scenePos().y()),
            ("inputs", [s.serialize() for s in self.inputs]),
            ("outputs", [s.serialize() for s in self.outputs]),
            ("content", self.content.serialize()),
            ("parent", {} if self.parent is None else self.parent.serialize())
        ])

    def deserialize(self, data, hashmap={}):
        self.id = data["id"]
        hashmap[data["id"]] = self

        self.icon = data["icon"]
        self.title = data["title"]
        self.set_pos(data["pos_x"], data["pos_y"])

        # set inputs and outputs
        data["inputs"].sort(key=lambda s: s["index"] + Position[s["position"]].value * 1000)
        data["outputs"].sort(key=lambda s: s["index"] + Position[s["position"]].value * 1000)

        self.inputs = []
        for s_data in data["inputs"]:
            socket = Socket(block=self,
                            index=s_data["index"],
                            position=Position[s_data["position"]],
                            socket_type=SocketType[s_data["socket_type"]])
            socket.deserialize(s_data, hashmap)
            self.inputs.append(socket)

        self.outputs = []
        for s_data in data["outputs"]:
            socket = Socket(block=self,
                            index=s_data["index"],
                            position=Position[s_data["position"]],
                            socket_type=SocketType[s_data["socket_type"]])
            socket.deserialize(s_data, hashmap)
            self.outputs.append(socket)

        self.content.deserialize(data["content"], hashmap)

        # set parent
        if "parent" in data.keys() and len(data["parent"]) > 0:
            self.parent = block_helper.create_block_parent(data["parent"], hashmap)

        return True
