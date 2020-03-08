#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# =========== #
# TOPIC_TAG #
# =========== #
# Model for topic tags in QiChat dialogue
#
# @author ES
# **

import logging
from copy import copy


class TopicTag(object):

    def __init__(self, name="", topic="", answers=[], feedbacks=[]):

        self.logger = logging.getLogger("TopicTag")

        self.name = name
        self.topic = topic
        self.answers = answers
        self.feedbacks = feedbacks

    def clone(self):
        return TopicTag(self.name, self.topic, copy(self.answers), copy(self.feedbacks))

    # ============== #
    # HELPER METHODS #
    # ============== #
    @property
    def to_dict(self):
        return {
            'name': self.name,
            'topic': self.topic,
            'answers': self.answers,
            'feedbacks': self.feedbacks
        }

    @staticmethod
    def create_topic_tag(tag_dict):
        topic_tag = None

        if tag_dict:
            topic_tag = TopicTag()
            topic_tag.name = tag_dict["name"]
            topic_tag.topic = tag_dict["topic"]
            if 'answers' in tag_dict.keys():
                topic_tag.answers = tag_dict['answers']
            if 'feedbacks' in tag_dict.keys():
                topic_tag.feedbacks = tag_dict['feedbacks']

        return topic_tag
