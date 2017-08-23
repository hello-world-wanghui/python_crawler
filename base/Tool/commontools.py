#! /usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
import numpy
from datetime import datetime, timedelta
from dateutil import relativedelta

class commontools():
    """
    通用的工具
    """
    def min_date_str(self):
        """
        最小时间string
        :return:
        """
        return '1970-01-01 00:00:00'

    def min_date(self):
        """
        最小时间
        :return:
        """
        return self.convert_to_date(self.min_date_str())

    def convert_to_date(self, date_str=''):
        """
        Date str to date
        """
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

    def today(self):
        """
        today on 00:00:00
        :return:
        """
        return datetime.today()

    def yesterday(self):
        """
        yesterday on 00:00:00
        """
        return self.today() - timedelta(days=1)

    def writefile(self, file_url, filename, filedata):
        file_path = os.path.join(file_url, filename)
        with open(file_path, "wb") as f:
            f.write(filedata)