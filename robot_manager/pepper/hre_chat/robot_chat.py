#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# ========== #
# ROBOT_CHAT #
# ========== #
# Model class for the Robot Chat
#
# @author ES
# **

import dialogflow_v2 as dialogflow
import es_common.hre_config as pconfig
from chat_config import *
import logging
from google.api_core.exceptions import InvalidArgument
from google.oauth2 import service_account


class RobotChatAgent(object):
    def __init__(self, project_id=DIALOGFLOW_PROJECT_ID, session_id='pid', credentials_file=GOOGLE_CREDENTIALS_FILE):
        self.logger = logging.getLogger(pconfig.logger_name)
        self._create_session(project_id, session_id, credentials_file)

    def _create_session(self, project_id=DIALOGFLOW_PROJECT_ID, session_id='pid',
                        credentials_file=GOOGLE_CREDENTIALS_FILE):
        self.project_id = project_id
        self.session_id = session_id
        self.credentials = service_account.Credentials.from_service_account_file(credentials_file)

        self.session_client = dialogflow.SessionsClient(credentials=self.credentials)
        self.session = self.session_client.session_path(self.project_id, self.session_id)
        self.logger.info("Created session with path: {}".format(self.session))

    def get_intent_from_text(self, text, language_code=DIALOGFLOW_LANGUAGE_CODE):
        """
        Returns the response fulfillment text received from Dialogflow
        or None otherwise
        """
        if text is None:
            return None

        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        try:
            response = self.session_client.detect_intent(session=self.session, query_input=query_input)
            self.logger.info('=' * 20)
            self.logger.info('Query text: {}'.format(response.query_result.query_text))
            self.logger.info('Detected intent: {} (confidence: {})'.format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence))
            self.logger.info('Fulfillment text: {}'.format(response.query_result.fulfillment_text))
            return str(response.query_result.fulfillment_text)
        except InvalidArgument as e:
            self.logger.error("Error while getting dialogflow intent:")
            self.logger.error(e)

    def get_intent_from_audio(self, audio_file, language_code=DIALOGFLOW_LANGUAGE_CODE):
        """
        Returns fulfillment text or None otherwise
        """
        # TODO: complete this method
        return
