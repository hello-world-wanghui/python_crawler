#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os

configs = {
    'mongo': {
        'MONGO_URI': 'mongodb://spider2:ThE_eJedRE5a@dds-bp1d09d4b278ceb41.mongodb.rds.aliyuncs.com:3717,dds-bp1d09d4b278ceb42.mongodb.rds.aliyuncs.com:3717/original_data?replicaSet=mgset-3255385',
        'MONGO_DB': 'original_data',
    },

    "logfile": os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "logs"),
}