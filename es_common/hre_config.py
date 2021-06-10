#!/usr/bin/env python
# -*- coding: utf-8 -*-
#**
#
# =========== #
# HRE_CONFIG #
# =========== #
# Config file with default data 
# ==> TODO: replace by YAML or .INI
#
# @author ES
#**

from python2.client import Python2
py2 = Python2('/usr/local/bin/python')

logger_name = 'hre_logger'

mongo_scope = py2.exec("""
import os
import pymongo
import functools

class Py2Helper(object):
    def __init__(self):
        self.client = pymongo.MongoClient(os.environ['CHANGE_STREAM_DB'])
        self.db = self.client["InteractionBlocksDB"]
        self.robot_collection = self.db.collection["RobotCollection"]

        self.people_in_zones_id = None

    def insert_block_completed(self, val=None):
        self.robot_collection.insert_one({'blockCompleted': 1})

    def insert_user_answer(self, val=None):
        if val is not None:
            self.robot_collection.insert_one({'userAnswer': val})

    def insert_people(self, event_name=None, subscriber_identifier=None):
        self.robot_collection.insert_one({'updatePeople': 1})
""")

# NAOQI properties
robot_ip = '127.0.0.1' # Replace by the robot IP
robot_tablet_ip = '198.18.0.1'
naoqi_port = 9559

# Sound settings
sound_peak = 14000
sound_sensitivity = 0.9

# Behavioral parameters
default_proxemics = 1.25 # in meters
proxemics_initial_value = 0.25
proxemics_multiplier = 0.25
proxemics_range = [0.25, 2.75]
default_voice_speed = 100
voice_speed_range = [40, 500]
default_voice_pitch = 1
voice_pitch_range = [0.5, 2.0]
default_voice_volume = 60
voice_volume_range = [0, 90] # % > 80 introduce clipping in audio!
volume_increase = 5

# face tracker
tracker_divert_time = 4 # in sec
divert_look_indexes = [0, 1] # [x, y, z]
divert_look_threshold = 0.3
robot_frame = 1 # [0, 1, 2] = [torso, world, robot]
default_face_width = 0.2

# Dialog app properties
app_name = "hre_dialog"
speech_recognition_user = "HRE_PEPPER"

# COLOR
ocean_color_rgb = 'rgb(7, 64, 128)'
warning_color_rgb = 'rgb(253, 128, 8)' # tangerine
default_color_rgb = 'rgb(236, 236, 236)' # grey

# Image properties
image_ext = "jpg"
image_name = 'PepperCamera'
output_dir = '/path/to/output/dir'
video_device = "ALVideoDevice"
welcome_image =  "apps/hre_dialog/pics/welcome.jpg" #"apps/images/welcome.jpg"
captured_picture_path = "apps/recordings/pics/pImage.jpg"
captured_picture_directory = "/home/nao/.local/share/PackageManager/apps/recordings/html/pics/"
captured_picture_name = "pImage"
fps = 30

# Logs
logs_directory = 'logs/dbs'

# Interaction blocks
SELECT_OPTION = "-- SELECT --"
# [file for _,_,i in os.walk('../hre_dialog') for file in i if (file.endswith('.html'))]