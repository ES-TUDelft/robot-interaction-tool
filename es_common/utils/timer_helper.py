#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# ============ #
# TIMER_HELPER #
# ============ #
# Helper class for timing events
#
# @author ES
# **

import logging
import time
import es_common.hre_config as pconfig


class TimerHelper(object):
    def __init__(self):
        self.logger = logging.getLogger(pconfig.logger_name)
        self.start_time, self.end_time = 0, 0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()

    def reset(self):
        self.start_time, self.end_time = 0, 0
