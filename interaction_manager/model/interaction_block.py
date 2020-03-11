#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# ================= #
# Interaction_BLOCK #
# ================= #
# Model for the interaction blocks.
#
# @author ES
# **
import logging
from collections import OrderedDict

from interaction_manager.enums.block_enums import SocketType
from interaction_manager.model.behavioral_parameters import BehavioralParameters
from es_common.datasource.serializable import Serializable
from es_common.model.tablet_page import TabletPage
from es_common.model.topic_tag import TopicTag
import copy


class InteractionBlock(Serializable):
    def __init__(self, name=None, stage=None, topic_tag=None, tablet_page=None, icon_path=None,
                 behavioral_parameters=None, block=None):
        super(InteractionBlock, self).__init__()

        self.logger = logging.getLogger("Interaction Block")

        self.name = "start" if name is None else name
        self.stage = "Opening" if stage is None else stage
        self.topic_tag = TopicTag() if topic_tag is None else topic_tag
        self.tablet_page = TabletPage() if tablet_page is None else tablet_page

        self.icon_path = None
        self.set_icon_path(icon_path)

        self.behavioral_parameters = BehavioralParameters() if behavioral_parameters is None else behavioral_parameters
        self.block = block

        self.interaction_start_time = 0
        self.interaction_end_time = 0

    def set_behavioral_parameters(self, p_name, behavioral_parameters):
        self.behavioral_parameters.set_parameters(p_name, behavioral_parameters)

    def clone(self):
        block = InteractionBlock()
        block.name = self.name
        block.message = self.message
        block.stage = self.stage
        block.topic_tag = self.topic_tag.clone()
        block.tablet_page = self.tablet_page.clone()
        block.icon_path = self.icon_path
        block.behavioral_parameters = self.behavioral_parameters.clone()
        block.block = copy.copy(self.block)

        block.interaction_start_time = self.interaction_start_time
        block.interaction_start_time = self.interaction_end_time

        return block

    def set_icon_path(self, icon_path):
        # TODO: use config file to retrieve the path
        if icon_path is None:
            self.icon_path = ":/hreresources/pepper-icons/pepper-standing.png"
        elif 'hreresources' in icon_path:
            self.icon_path = icon_path
        else:
            self.icon_path = ":/hreresources/pepper-icons/{}".format(icon_path)

    def get_connected_blocks(self, socket_type=SocketType.OUTPUT):
        return self.block.get_connected_blocks(socket_type=socket_type)

    def get_connected_interaction_blocks(self, socket_type=SocketType.OUTPUT):

        blocks = self.get_connected_blocks(socket_type)
        if blocks is not None:
            return [b.parent for b in blocks]
        return None

    def get_next_interaction_block(self, execution_result=None):
        next_block = None
        try:
            int_blocks = self.get_connected_interaction_blocks(socket_type=SocketType.OUTPUT)

            if int_blocks is None or len(int_blocks) == 0:  # no next block available!
                return None

            # in the absence of a condition
            if execution_result is None or execution_result == "":
                # select first if possible
                next_block = int_blocks[0]  # we already verified the len to be > 0
            else:
                # check the answers
                for i in range(len(self.topic_tag.answers)):
                    # if the result is in the answers ==> go to appropriate interaction block
                    if execution_result.lower() in self.topic_tag.answers[i].lower():
                        next_block = self._get_block_by_id(int_blocks, self.topic_tag.goto_ids[i])
                        break
        except Exception as e:
            self.logger.error("Error while attempting to get the next block! {}".format(e))
        finally:
            self.logger.debug("Next block is: {} | {}".format(0 if next_block is None else next_block.title,
                                                              next_block))
            return next_block

    def set_selected(self, val):
        if val is not None:
            self.block.set_selected(val)

    def _get_block_by_id(self, b_lst, target_id):
        for b in b_lst:
            if b.id == target_id:
                return b
        return None

    # ===========
    # PROPERTIES
    # ===========
    @property
    def icon(self):
        return self.icon_path.replace(":/hreresources/pepper-icons/", "")

    @property
    def speech_act(self):
        return self.behavioral_parameters.speech_act

    @speech_act.setter
    def speech_act(self, speech_act):
        self.behavioral_parameters.speech_act = speech_act

    @property
    def message(self):
        # uses the speech_act property above to return the message
        return self.speech_act.message

    @message.setter
    def message(self, value):
        self.speech_act.message = value

    @property
    def gestures(self):
        return self.behavioral_parameters.gesture.gestures

    @gestures.setter
    def gestures(self, value):
        self.behavioral_parameters.gesture.gestures = value

    @property
    def gestures_type(self):
        return self.behavioral_parameters.gestures_type

    @gestures_type.setter
    def gestures_type(self, gestures_type):
        self.behavioral_parameters.gestures_type = gestures_type

    @property
    def description(self):
        return "" if self.block is None else self.block.description

    @description.setter
    def description(self, desc):
        if self.block is not None:
            self.block.description = desc

    @property
    def title(self):
        return "" if self.block is None else self.block.title

    @property
    def to_dict(self):
        block_dict = OrderedDict([
            ("id", self.id),
            ("name", self.name),
            ("stage", self.stage),
            ("topic_tag", self.topic_tag.to_dict),
            ("tablet_page", self.tablet_page.to_dict),
            ("icon_path", self.icon_path),
            ("behavioral_parameters", self.behavioral_parameters.to_dict),
            ("block", self.block.id),
            ("interaction_start_time", self.interaction_start_time),
            ("interaction_end_time", self.interaction_end_time)
        ])

        return block_dict

    @staticmethod
    def create_interaction_block(block_dict):
        if block_dict:
            block = InteractionBlock(name=block_dict['name'],
                                     stage=block_dict['stage'],
                                     topic_tag=TopicTag.create_topic_tag(tag_dict=block_dict['topic_tag']),
                                     tablet_page=TabletPage.create_tablet_page(page_dict=block_dict["tablet_page"]),
                                     icon_path=block_dict['icon_path']
                                     )
            if 'behavioral_parameters' in block_dict.keys():  # otherwise, keep default values
                block.behavioral_parameters = BehavioralParameters.create_behavioral_parameters(
                    beh_dict=block_dict['behavioral_parameters'])
            if any('interaction' in k for k in block_dict.keys()):
                block.interaction_start_time = block_dict['interaction_start_time']
                block.interaction_end_time = block_dict['interaction_end_time']

            return block

        return None

    ###
    # SERIALIZATION
    ###
    def serialize(self):
        return self.to_dict

    def deserialize(self, data, hashmap={}):
        self.id = data["id"]
        hashmap[data["id"]] = self

        self.block = hashmap[data["block"]]

        return True
