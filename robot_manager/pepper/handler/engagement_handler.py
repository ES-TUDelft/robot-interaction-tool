#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# ================== #
# ENGAGEMENT_HANDLER #
# ================== #
# Handler class for controlling the robot's engagement
#
# @author ES
# **

import logging

import es_common.hre_config as pconfig
from robot_manager.pepper.enums.engagement_enums import EngagementMode, EngagementZone
from naoqi import ALProxy
import functools


class EngagementHandler(object):

    def __init__(self, session=None, robot_ip=pconfig.robot_ip, port=pconfig.naoqi_port):
        self.logger = logging.getLogger(pconfig.logger_name)

        self.session = session
        self.robot_ip = robot_ip
        self.port = port

        self.__memory, self.__people_perception, self.__face_detection = (None, ) * 3
        self.__basic_awareness, self.__engagement_zones, self.__movement_detection = (None,) * 3

        self.__tracker = None

    def set_engagement(self, mode=EngagementMode.UNENGAGED):
        self.basic_awareness.setEngagementMode(mode.value)

    def engage(self, person_id):
        self.basic_awareness.engagePerson(person_id)

    def get_people(self, zone=EngagementZone.ZONE1):
        print("{} {}".format(zone.name, zone.value))
        return self.memory.getData(zone.value)

    def face_tracker(self, start=True, face_width=pconfig.default_face_width):
        if start is True:
            target_name = "Face"
            # register target
            self.tracker.registerTarget(target_name, face_width)
            # start tracker
            self.tracker.track(target_name)
        else:
            self.tracker.stopTracker()
            self.tracker.unregisterAllTargets()

    def divert_look(self, gaze_pattern=None, frame=pconfig.robot_frame, thresh=pconfig.divert_look_threshold):
        if not (gaze_pattern is None):
            multiplier = 1.5 if gaze_pattern.value > 1 else gaze_pattern.value
            thresh = thresh * multiplier
            # self.logger.info("Gaze thresh is now: {}".format(thresh))
        pos = self.tracker.getTargetPosition(frame)

        if len(pos) > 0:
            # divert look
            pos = [pos[0] + thresh, pos[1] + thresh, pos[2]]
            self.tracker.lookAt(pos, frame, 0.1, False)
            # move back
            pos = [pos[0] - thresh, pos[1] - thresh, pos[2]]
            self.tracker.lookAt(pos, frame, 0.1, False)

    def tracking(self, enable=True):
        if self.face_detection.isTrackingEnabled() is enable:
            self.logger.info("Tracking was already {}".format("enabled." if enable is True else "disabled."))
        else:
            self.face_detection.enableTracking(enable)
            self.logger.info("Tracking is {}".format("enabled." if enable is True else "disabled."))

    def subscribe(self):
        self.people_perception.subscribe("EngagingPeople")

    def unsubscribe(self):
        self.people_perception.unsubscribe("EngagingPeople")


    """
    MEMORY
    """

    @property
    def memory(self):
        if self.__memory is None:
            self.__memory = ALProxy("ALMemory", self.robot_ip,
                                    self.port) if self.session is None else self.session.service("ALMemory")
        return self.__memory

    """
    PEOPLE_PERCEPTION
    """

    @property
    def people_perception(self):
        if self.__people_perception is None:
            self.__people_perception = ALProxy("ALPeoplePerception", self.robot_ip,
                                               self.port) if self.session is None else self.session.service(
                "ALPeoplePerception")
        return self.__people_perception

    """
    FACE_DETECTION
    """

    @property
    def face_detection(self):
        if self.__face_detection is None:
            # TODO: replace by a method call!
            self.people_perception  # needed
            self.__face_detection = ALProxy("ALFaceDetection", self.robot_ip,
                                            self.port) if self.session is None else self.session.service(
                "ALFaceDetection")
        return self.__face_detection

    """
    TRACKER
    """

    @property
    def tracker(self):
        if self.__tracker is None:
            self.__tracker = ALProxy("ALTracker", self.robot_ip,
                                     self.port) if self.session is None else self.session.service("ALTracker")
        return self.__tracker

    """
    AWARENESS
    """

    @property
    def basic_awareness(self):
        if self.__basic_awareness is None:
            self.__basic_awareness = ALProxy("ALBasicAwareness", self.robot_ip,
                                             self.port) if self.session is None else self.session.service(
                "ALBasicAwareness")
        return self.__basic_awareness

    """
    ENGAGEMENT_ZONES
    """

    @property
    def engagement_zones(self):
        if self.__engagement_zones is None:
            self.__engagement_zones = ALProxy("ALEngagementZones", self.robot_ip,
                                              self.port) if self.session is None else self.session.service(
                "ALEngagementZones")
        return self.__engagement_zones

    """
    MOVEMENT_DETECTION
    """

    @property
    def movement_detection(self):
        if self.__movement_detection is None:
            self.__movement_detection = ALProxy("ALMovementDetection", self.robot_ip,
                                                self.port) if self.session is None else self.session.service(
                "ALMovementDetection")
        return self.__movement_detection
