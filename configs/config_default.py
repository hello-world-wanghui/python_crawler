#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

configs = {
    'mongo': {
        'MONGO_URI': 'localhost:27017',
        'MONGO_DB': 'crawler_python',
    },
    "mysql": {
        "host": "localhost",
        "port": "3306",
        "user": "root",
        "passwd": "123456",
        "db": "crawler_python",
    },
    "PROJECT_PATH": PROJECT_PATH,

    "logfile": os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "logs"),
}
