#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **
#
# ========================= #
# CONFIG_HELPER #
# ========================= #
# Helper class for accessing the app config.
#
# @author ES
# **

import logging

import yaml


####
# Logger
###
def _setup_logger():
    logging.basicConfig(level=logging.DEBUG)
    return logging.getLogger('app_logger')


logger = _setup_logger()


####
# APP PROPERTIES
###
def get_app_properties():
    props = None
    try:
        with open("interaction_manager/properties/app.yaml", 'r') as ymlfile:
            props = yaml.load(ymlfile, Loader=yaml.SafeLoader)
    except Exception as e:
        logger.error("Error while opening the app properties file! {}".format(e))
    finally:
        return props


app_properties = get_app_properties()


def get_topics():
    # returns dict of gestures: 
    # names are the keys and path are values
    return _get_property(app_properties, 'topics')


####
# MONGO DB PROPERTIES
###
def _get_db_properties():
    props = None
    try:
        with open("interaction_manager/properties/db.yaml", 'r') as ymlfile:
            props = yaml.load(ymlfile, Loader=yaml.SafeLoader)
    except Exception as e:
        logger.error("Error while opening the db properties file! {}".format(e))
    finally:
        return props


db_properties = _get_db_properties()


def get_db_mongo_settings():
    # returns dict of gestures: 
    # names are the keys and path are values
    return _get_property(db_properties, 'mongodb')


####
# Block Properties
###
def _get_block_properties():
    props = None
    try:
        # on Linux use: block-linux.yaml
        with open("interaction_manager/properties/block.yaml", 'r') as yaml_file:
            props = yaml.load(yaml_file, Loader=yaml.SafeLoader)
    except Exception as e:
        logger.error("Error while opening the block properties file! {}".format(e))
    finally:
        return props


block_props = _get_block_properties()


def get_colors():
    return block_props["colors"]


def get_icons():
    return block_props["icons"]


def get_patterns():
    return block_props["patterns"]


def get_block_mimetype():
    return block_props["block_mimetype"]


def get_block_size_settings():
    return block_props["size"]["block"]


def get_socket_size_settings():
    return block_props["size"]["socket"]


####
# BEHAVIORS PROPERTIES
###
def get_behaviors_properties():
    props = None
    try:
        with open("interaction_manager/properties/behaviors.yaml", 'r') as ymlfile:
            props = yaml.load(ymlfile, Loader=yaml.SafeLoader)
    except Exception as e:
        logger.error("Error while opening the behaviors properties file! {}".format(e))
    finally:
        return props


behaviors_properties = get_behaviors_properties()


def get_actions():
    # returns dict of gestures: 
    # names are the keys and path are values
    return _get_property(behaviors_properties, 'actions')


def get_gestures():
    # returns dict of gestures: 
    # names are the keys and path are values
    return _get_property(behaviors_properties, 'gestures')


####
# Config
###
def _get_config():
    config = None
    try:
        with open("interaction_manager/properties/config.yaml", 'r') as yaml_file:
            config = yaml.load(yaml_file, Loader=yaml.SafeLoader)
    except Exception as e:
        logger.error("Error while opening the config file! {}".format(e))
    finally:
        return config


sys_config = _get_config()


###
# HELPER METHODS
###
def _get_property(props_dict, key):
    prop = None
    try:
        prop = props_dict[key]
    except Exception as e:
        logger.error("Error while getting '{}' from '{}' | {}".format(key, props_dict, e))
    finally:
        return prop
