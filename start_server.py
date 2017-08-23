#! /usr/bin/env python
# -*- coding: utf-8 -*-

from Scheduling.Scheduling_start import Scheduling_start
import datetime
import sys
from configs.logconfig import FinalLogger
import os
from configs import config

reload(sys)
sys.setdefaultencoding('utf-8')

configs = config.configs
log_path = configs.get("logfile")
loggingname = "apscheduler.executors.default"
fmt = '%(asctime)s %(name)s %(levelname)s: %(funcName)s %(lineno)d %(message)s'
log_file = os.path.join(log_path, "apscheduler.log")
logger = FinalLogger().getLogger(loggingname=loggingname, fmt=fmt, log_file=log_file)

Scheduling = Scheduling_start(logger)

Scheduling.add_job(job_path="job.crawler_job.text_job", classname="text_job", job_id="1",
                   trigger="date", args=[])

Scheduling.add_job(job_path="job.crawler_job.text_job", classname="text_job", job_id="1",
                   trigger="cron", hour="2", args=[])

while True:
    pass
