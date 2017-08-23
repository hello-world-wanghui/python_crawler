#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import json
from tornado import web, httpserver, ioloop, gen
from Scheduling.Scheduling_start import Scheduling_start
from configs.config import configs
import os

class index(web.RequestHandler):
    """
    index
    """
    def get(self, *args, **kwargs):
        self.render("index.html")

class get_projects(web.RequestHandler):
    """
    获取项目列表
    """
    def get(self, *args, **kwargs):
        path = configs.get("PROJECT_PATH")
        files = os.listdir(os.path.join(path, "job\\crawler_job"))

urls = [
    ("/index", index),
    ("/index.html", index),
    ("/index.htm", index),
    ("/", index),
]
