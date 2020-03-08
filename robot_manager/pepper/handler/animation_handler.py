#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# ================= #
# ANIMATION_HANDLER #
# ================= #
# Handler class for animating the robot (controlling its behaviors)
#
# @author ES
# **

import logging

import es_common.hre_config as pconfig
from robot_manager.pepper.enums.motion_enums import HeadMotion, Animation, AutonomousLife
from naoqi import ALProxy


class AnimationHandler(object):
    def __init__(self, session=None, robot_ip=pconfig.robot_ip, port=pconfig.naoqi_port):

        self.logger = logging.getLogger(pconfig.logger_name)
        if session is None:
            self.motion = ALProxy("ALMotion", robot_ip, port)
            self.navigation = ALProxy("ALNavigation", robot_ip, port)
            self.posture = ALProxy("ALRobotPosture", robot_ip, port)
            self.awareness = ALProxy('ALBasicAwareness', robot_ip, port)
            self.autonomous_life = ALProxy('ALAutonomousLife', robot_ip, port)
            self.animation_player = ALProxy("ALAnimationPlayer")
        else:
            self.motion = session.service("ALMotion")
            self.navigation = session.service("ALNavigation")
            self.posture = session.service("ALRobotPosture")
            self.awareness = session.service('ALBasicAwareness')
            self.autonomous_life = session.service('ALAutonomousLife')
            self.animation_player = session.service("ALAnimationPlayer")

        self.motion_proxy = ALProxy("ALMotion", robot_ip,
                                    int(port))  # needed for using 'post' when combining mvt with speech/gestures

    def wakeup(self, awareness=True, breathing=False):
        # Wake up robot
        self.motion.wakeUp()

        # Collision detection
        self.motion.setExternalCollisionProtectionEnabled("All", True)
        self.set_autonomous_life(state=AutonomousLife.SOLITARY)
        # Start/Stop Awareness
        # self.set_awareness(enable = awareness)

        # Breathing
        # self.set_breathing(enable = breathing)

        # stand posture
        # self.reset_posture()

    def reset_posture(self):
        # TODO: check if it's needed to reset the posture
        pass
        # Send robot to Stand Init
        # self.posture.goToPosture("StandInit", 0.5)

        # go to an init head pose.
        # self.reset_head_pose()

    def is_awake(self):
        return self.motion.robotIsWakeUp()

    def is_aware(self):
        return self.awareness.isEnabled()

    def set_autonomous_life(self, state=AutonomousLife.SOLITARY):
        to_log = ("Going from {} state".format(self.autonomous_life.getState()))
        self.autonomous_life.setState(state.value)
        self.logger.info("{} to {} state.".format(to_log, self.autonomous_life.getState()))

    def set_breathing(self, enable=False):
        self.motion.setBreathEnabled('Body', enable)

    def is_breathing_enabled(self):
        return self.motion.getBreathEnabled('Body')

    def set_awareness(self, enable=False):
        # pause/resume awareness
        self.awareness.resumeAwareness() if enable is True else self.awareness.pauseAwareness()
        # Start/Stop Awareness
        # self.awareness.startAwareness() if enable is True else self.awareness.stopAwareness()

    def rest(self):
        self.motion.rest()

    def reset_head_pose(self):
        # go to an init head pose.
        joints = [HeadMotion.YAW._name, HeadMotion.PITCH._name]
        angles = [0.0, pconfig.default_head_pitch]
        times = [1.0, 1.0]
        try:
            self.motion.angleInterpolation(joints, angles, times, True)
        except Exception as e:
            self.logger.error("* Error while trying to reset the head position")
            self.logger.error(e)

    def animate(self, animation=Animation.WAVE):
        if animation is None:
            return None
        try:
            self.animation_player.run(animation.value)
        except Exception as e:
            self.logger.error("* Error while trying to execute the animation tag: '" + str(animation) + "'")
            self.logger.error(e)

    def check_animation(self, animation_name):
        if animation_name is None:
            self.logger.error("* Animation tag was NONE...")
        try:
            self.animation_player.run(animation_name)
        except Exception as e:
            self.logger.error("* Error while trying to execute the animation tag: '{}'".format(animation_name))
            self.logger.error(e)

    def move_to(self, x=0, y=0, theta=0):
        # self.motion.setStiffnesses("Body", 1.0)
        self.logger.info('Attempting to move by [x, y, theta] = [{}, {}, {}]'.format(x, y, theta))
        self.motion.moveTo(x, y, theta)
        # self.motion_proxy.post.moveTo(x, y, theta)

    def finish_move(self):
        self.motion_proxy.waitUntilMoveIsFinished()

    def _get_angle(self, angle=0.0, joint_range=[0.0, 0.0]):
        return angle if joint_range[0] <= angle <= joint_range[1] else 0.0

    def get_angles(self, joint="Body", use_sensors=True):
        return self.motion.getAngles(joint, use_sensors)
