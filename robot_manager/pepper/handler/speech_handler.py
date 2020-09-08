#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# ============== #
# SPEECH_HANDLER #
# ============== #
# Handler class for controlling the robot's dialog and speech acts
#
# @author ES
# **

import logging

import es_common.hre_config as pconfig
from es_common.enums.voice_enums import VoiceTag, VoiceName
from robot_manager.pepper.enums.engagement_enums import DialogTopic


class SpeechHandler:

    def __init__(self, session):

        self.logger = logging.getLogger("Speech Handler")

        self.tts = session.service("ALTextToSpeech")
        self.animated_speech = session.service("ALAnimatedSpeech")

        # self.speech_recognition = session.service("ALSpeechRecognition")
        # self.sound_detector = session.service("ALSoundDetection")
        self.audio = session.service("ALAudioDevice")
        self.dialog = session.service("ALDialog")
        self.memory = session.service("ALMemory")

        # self.tts.setParameter('speed', 150)
        # self.animated_speech.setParameter('speed', 150)

        # Subscribe to get last input
        self.lastInput = self.memory.subscriber("Dialog/LastInput")
        # self.logger.info("\n\nBodyId: {}\n\n".format(self.memory.getData("Device/DeviceList/ChestBoard/BodyId")))
        self.lastInput.signal.connect(self.log)

        # Notify when topic is completed
        self.block_completed = self.memory.subscriber("blockCompleted")
        self.block_completed.signal.connect(self.exit_topic)  # not important (for testing purposes)

        # self.sound_detected = self.memory.subscriber("SoundDetected")
        # self.sound_detected.signal.connect(self.log)

        # listen to webpage loaded
        self.pageLoaded = self.memory.subscriber("pageLoaded")
        self.pageLoaded.signal.connect(self.webpage_loaded)

        self.answer_listener = self.memory.subscriber("userAnswer")
        self.answer_listener.signal.connect(self.set_user_answer)  # for testing purposes

        self.current_topic = None

    # ======
    # SPEECH
    # ======
    def say(self, message="Hi"):
        self.logger.info("Message from say: {}".format(message))
        return False if message is None else self.tts.say(message)

    def animated_say(self, message=None, animation_name=None, robot_voice=None):
        if message is None:
            return False

        try:
            self.setup_voice(robot_voice=robot_voice)
            if animation_name is None:
                success = self.animated_speech.say(message, {"bodyLanguageMode": "contextual"})  # vs random
            else:
                success = self.animated_speech.say('^start({}) {} ^wait({})'.format(animation_name,
                                                                                    message,
                                                                                    animation_name),
                                                   {"bodyLanguageMode": "contextual"})
            self.setup_voice(reset=True)
            return success
        except Exception as e:
            self.logger.error("Error while executing animated message! {}".format(e))

    def customized_say(self, interaction_block=None):
        if interaction_block is None: return

        # update the tablet page
        self._set_page_fields(interaction_block.tablet_page)

        # Set up the robot voice
        robot_voice = interaction_block.behavioral_parameters.voice
        self.setup_voice(robot_voice=robot_voice)

        # to_say = "\\{}={}\\\\{}={}\\\\{}={}\\\\{}={}\\\\{}={}\\ {}".format(
        #            VoiceTag.SPEED.value, robot_voice.speed,
        #            VoiceTag.PITCH.value, robot_voice.pitch, 
        to_say = "\\{}={}\\ {}".format(
            VoiceTag.PROSODY.value, "S" if robot_voice.prosody.value is 1 else "W",
            interaction_block.message)

        self.logger.info("Message = {}".format(to_say))

        animation_name = None if interaction_block.gestures is None else interaction_block.gestures[
            interaction_block.gestures_type.name.lower()]

        success = self.animated_say(message=to_say, animation_name=animation_name)

        self.setup_voice(reset=True)
        return success

    # ======
    # VOICE
    # ======
    def setup_voice(self, robot_voice=None, reset=False):
        if reset is True:
            # reset the parameters
            self.set_voice_speed(reset=True)
            self.set_voice_pitch(reset=True)
        elif robot_voice is not None:
            self.set_volume(level=robot_voice.volume)
            self.set_voice_speed(speed=robot_voice.speed)
            self.set_voice_pitch(pitch=robot_voice.pitch)

    def set_volume(self, level=0.5):
        self.audio.setOutputVolume(int(level) if level > 1 else int(level * 100))  # vol <= 100
        self.logger.info("Volume set to: {}".format(self.audio.getOutputVolume()))

    def set_voice_name(self, name=VoiceName.CLAIRE, reset=False):
        self.tts.setVoice(name.value)

    def set_voice_speed(self, speed=pconfig.default_voice_speed, reset=False):
        if reset is True:
            self.tts.resetSpeed()
        else:
            self.tts.setParameter("speed", speed if pconfig.voice_speed_range[0] <= speed <= pconfig.voice_speed_range[
                1] else pconfig.default_voice_speed)

    def set_voice_pitch(self, pitch=pconfig.default_voice_pitch, reset=False):
        self.tts.setParameter("pitchShift", pitch if pconfig.voice_pitch_range[0] <= pitch <= pconfig.voice_pitch_range[
            1] else pconfig.default_voice_pitch)

    def set_language(self, name='English'):
        self.tts.setLanguage(name)
        self.dialog.setLanguage(name)

    def log(self, value):
        self.logger.info("Pepper heard: {}".format(value))

    # =======
    # DIALOG
    # =======
    def start_dialog(self):
        try:
            for d_topic in DialogTopic.values():
                topic_name = self.dialog.loadTopic(d_topic)
                self.logger.info("TOPIC: {}".format(topic_name))
            self.dialog.subscribe("hre_dialog")
            self.logger.info("Started the dialog successfully.")
        except Exception as e:
            self.logger.error("Error while starting dialog! {}".format(e))

    def exit_topic(self, val):
        self.logger.info("Exit Topic called: {}".format(val))
        # self.deactivate_topics()

    def deactivate_topics(self):
        # Deactivate active topics
        for topic in self.dialog.getActivatedTopics():
            try:
                self.dialog.deactivateTopic(topic)
            except Exception as e:
                self.logger.error("Error while deactivating {}. {}".format(topic, e))
        self.current_topic = None
        self.logger.info("Topics are deactivated.")

    def unload_topics(self):
        # Unload all topics
        for topic in self.dialog.getAllLoadedTopics():
            try:
                self.dialog.unloadTopic(topic)
            except Exception as e:
                self.logger.error("Error while unloading {}. {}".format(topic, e))
        self.logger.info("Topics are unloaded.")

    def pause_dialog(self):
        # Deactivate and Unload existing topics
        self.deactivate_topics()

    def stop_dialog(self):
        # Deactivate and Unload existing topics
        self.deactivate_topics()
        self.unload_topics()

        try:
            self.dialog.stopDialog()
            self.dialog.unsubscribe("hre_dialog")
            self.logger.info("Stopped the dialog.")
        except Exception as e:
            self.logger.error("Error while stopping dialog. {}".format(e))

    def webpage_loaded(self, value):
        self.logger.info("INPUT: {}".format(value))
        # self.activate_topic(topic_name = input)

    def activate_topic(self, interaction_block):
        if interaction_block is None:
            return None

        topic_tag = interaction_block.topic_tag
        try:
            self.setup_voice(robot_voice=interaction_block.behavioral_parameters.voice)

            # 1) Deactivate active topics
            self.deactivate_topics()

            # 2) activate needed topic
            self.dialog.activateTopic(topic_tag.topic)

            # 3) set custom fields and insert data in memory
            self._set_topic_fields(custom_message=interaction_block.message,
                                   custom_animation=interaction_block.gestures[
                                       interaction_block.gestures_type.name.lower()],
                                   topic_tag=topic_tag)
            self._set_page_fields(interaction_block.tablet_page)

            # set focus to the topic
            self.dialog.setFocus(topic_tag.topic)
            self.current_topic = topic_tag.topic
            self.logger.info("Activated topic: {}".format(self.dialog.getActivatedTopics()))

            # 4) Activate the tag
            if self.is_valid_string(topic_tag.name):
                self.dialog.gotoTag(topic_tag.name, topic_tag.topic)

        except Exception as e:
            self.logger.error("Error while loading topic {}. {}".format(topic_tag.topic, e))

    def set_user_answer(self, value):
        self.logger.info("UserAnswer: {}".format(value))

    def _set_topic_fields(self, custom_message, custom_animation, topic_tag):
        # Insert valid values into memory
        if self.is_valid_string(custom_message):
            self.memory.insertData("customMessage", custom_message.strip())

        if self.is_valid_string(custom_animation):
            self.memory.insertData("customAnimation", custom_animation)

        # self._insert_array_into_memory(topic_tag.answers, "answer")
        self._set_concept(arr=topic_tag.answers, lang="enu", concept_name="answer")
        self._insert_array_into_memory(topic_tag.feedbacks, "feedback")

    def _set_concept(self, arr, lang="enu", concept_name="theconcept"):
        if arr is None: return

        for i in range(len(arr)):
            self.logger.info(
                "{}{} | {} | {}".format(concept_name, (i + 1), lang, [s.strip() for s in arr[i].split(';')]))
            self.dialog.setConcept("{}{}".format(concept_name, (i + 1)), lang, [s.strip() for s in arr[i].split(';')])

    def _insert_array_into_memory(self, arr, field_name="field"):
        if arr is None: return

        # insert in the form: field{i} = arr[i]
        for i in range(len(arr)):
            to_insert = "{}{}".format(field_name, (i + 1))
            if self.is_valid_string(arr[i]):
                to_insert = "{}{}".format(field_name, (i + 1))
                self.logger.info("**** {} | {}".format(to_insert, arr[i]))
                self.memory.insertData(to_insert, arr[i])
            else:
                self.memory.insertData(to_insert, "")

    def _set_page_fields(self, page):
        # load the appropriate webpage on the tablet, if any
        if page is not None and self.is_valid_string(page.name):
            # self.logger.info(page.to_dict)
            self.memory.insertData("pageName", "{}".format(page.name))

            self.memory.insertData("pageImage",
                                   "pepper-standing.png" if self.is_valid_string(page.image) is False else page.image)

            self.memory.insertData("pageHeading", "{}".format(page.heading))
            self.memory.insertData("pageText", "{}".format(page.text))
            self.dialog.gotoTag("loadAndFillPageTag", "general")

    def is_valid_string(self, value):
        '''
        @return False if value is None or is equal to empty string; and True otherwise.
        '''
        return False if (value is None or value.strip() == "") else True

    def raise_event(self, event_name, event_value):
        self.logger.info("Raised event '{}' to load '{}'".format(event_name, event_value))
        self.memory.raiseEvent(event_name, event_value)
