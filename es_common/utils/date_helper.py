#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# =========== #
# DATE_HELPER #
# =========== #
# Helper class for date and time manipulation
#
# @author ES
# **

import datetime


def get_date_and_time(a_date=None):
    d = datetime.datetime.today() if a_date is None else a_date

    return "{} at {}".format(get_date(a_date=d), get_time(a_date=d))


def get_date(a_date=None):
    d = datetime.datetime.today() if a_date is None else a_date

    return "{0:%A}, {0:%B} {0:%d}, {0:%Y}".format(d)


def get_time(a_date=None):
    d = datetime.datetime.today() if a_date is None else a_date

    return "{0:%I:%M:%S}".format(d)


def get_daytime_message():
    d = datetime.datetime.now()
    if d.hour <= 12:
        return "Good Morning"
    elif 12 < d.hour <= 16:
        return "Good Afternoon"
    elif 16 < d.hour <= 20:
        return "Good Evening"
    else:
        return "Hello"
