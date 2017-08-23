#! /usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from job.job_base import job_base

class text_job(job_base):

    def run(self):
        print ("这是测试job")
        self.logger.info(self.settings)
        self.logger.info("text_job ")
        self.logger.info(self.http.proxies)