#! /usr/bin/env python
# -*- coding: utf-8 -*-

from view import Scheduler
from view import file_server
from view import home

urlheaders = []
urlheaders.extend(file_server.urls)
urlheaders.extend(Scheduler.urls)
urlheaders.extend(home.urls)
