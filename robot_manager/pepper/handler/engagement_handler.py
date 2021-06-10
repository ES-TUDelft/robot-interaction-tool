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


class EngagementHandler(object):

    def __init__(self, session):
        self.logger = logging.getLogger("Engagement Handler")

        self.session = session
        self.memory = self.session.service("ALMemory")
        self.people_perception = self.session.service("ALPeoplePerception")
        self.face_detection = self.session.service("ALFaceDetection")
        self.tracker = self.session.service("ALTracker")
        self.basic_awareness = self.session.service("ALBasicAwareness")
        self.engagement_zones = self.session.service("ALEngagementZones")
        self.movement_detection = self.session.service("ALMovementDetection")

        self.people_in_zones = self.memory.subscriber("EngagementZones/PeopleInZonesUpdated")
        self.people_in_zones_id = None

    def set_engagement(self, mode=EngagementMode.UNENGAGED):
        self.basic_awareness.setEngagementMode(mode.value)

    def engage(self, person_id):
        self.basic_awareness.engagePerson(person_id)

    def get_people(self, zone=EngagementZone.ZONE1):
        return self.memory.getData(zone.value)

    def face_tracker(self, start=True, face_width=pconfig.default_face_width):
        pass
        # if self.tracker is not None:
        #     try:
        #         if start is True:
        #             target_name = "Face"
        #             # register target
        #             self.tracker.registerTarget(target_name)
        #             # start tracker
        #             self.tracker.track(target_name)
        #         else:
        #             self.tracker.stopTracker()
        #             self.tracker.unregisterAllTargets()
        #     except Exception as e:
        #         self.logger.error("Error while using the face tracker: {}".format(e))

    def divert_look(self, gaze_pattern=None, frame=pconfig.robot_frame, thresh=pconfig.divert_look_threshold):
        pass
        # if not (gaze_pattern is None):
        #     multiplier = 1.5 if gaze_pattern.value > 1 else gaze_pattern.value
        #     thresh = thresh * multiplier
        #     # self.logger.info("Gaze thresh is now: {}".format(thresh))
        # pos = self.tracker.getTargetPosition(frame)
        #
        # if len(pos) > 0:
        #     # divert look
        #     pos = [pos[0] + thresh, pos[1] + thresh, pos[2]]
        #     self.tracker.lookAt(pos, frame, 0.1, False)
        #     # move back
        #     pos = [pos[0] - thresh, pos[1] - thresh, pos[2]]
        #     self.tracker.lookAt(pos, frame, 0.1, False)

    def tracking(self, enable=True):
        pass
        # if self.face_detection.isTrackingEnabled() is enable:
        #     self.logger.info("Tracking was already {}".format("enabled." if enable is True else "disabled."))
        # else:
        #     self.face_detection.enableTracking(enable)
        #     self.logger.info("Tracking is {}".format("enabled." if enable is True else "disabled."))

    def subscribe(self):
        try:
            py2_helper = pconfig.mongo_scope['Py2Helper']()

            # if self.people_in_zones is None:
            # self.people_in_zones = self.memory.subscriber("EngagementZones/PeopleInZonesUpdated")
            print("\nPeople in zones: {} | {}\n".format(self.people_in_zones, self.memory))

            self.people_in_zones.signal.connect(py2_helper.insert_people)

            self.people_perception.subscribe("EngagingPeople")

            self.logger.info("\nSuccessfully subscribed to engagement zones.\n")
        except Exception as e:
            self.logger.error("\nError while subscribing to people zones: {}\n".format(e))

    def unsubscribe(self):
        self.people_perception.unsubscribe("EngagingPeople")
        # self.people_in_zones.signal.disconnect(self.people_in_zones_id)
