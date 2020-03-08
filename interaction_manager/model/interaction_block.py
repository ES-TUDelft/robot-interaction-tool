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
from collections import OrderedDict

from interaction_manager.model.behavioral_parameters import BehavioralParameters
from es_common.datasource.serializable import Serializable
from es_common.model.tablet_page import TabletPage
from es_common.model.topic_tag import TopicTag
import copy


class InteractionBlock(Serializable):
    def __init__(self, name=None, stage=None, topic_tag=None, tablet_page=None, icon_path=None,
                 behavioral_parameters=None, block=None):
        super(InteractionBlock, self).__init__()

        self.name = "New Block" if name is None else name
        self.stage = "Opening" if stage is None else stage
        self.topic_tag = TopicTag() if topic_tag is None else topic_tag
        self.tablet_page = TabletPage() if tablet_page is None else tablet_page
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
