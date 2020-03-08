#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# =============== #
# MAIN_DIALOGFLOW #
# =============== #
# Class for testing dialogflow
# Should be called from the root directory 
# (check the credentials path in chat_config.py)
#
# @author ES
# **

import sys
import logging
from robot_chat import RobotChatAgent


def main():
    pepper_chat = RobotChatAgent()
    pepper_chat.get_intent_from_text("Hello, tell me a joke.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(filename)s:%(lineno)4d: %(message)s',
                        stream=sys.stdout)
    main()
