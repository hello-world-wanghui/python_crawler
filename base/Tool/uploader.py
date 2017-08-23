# -*- coding: utf-8 -*-
# coding=utf-8

import oss2
import logging
import os
from configs import config

# 阿里云oss 相关参数.
OSS_ACCESS_KEY = 'LTAITN0hCn7KBUzK'
OSS_ACCESS_KEY_SECRET = 'c8SOHjg15bkkW3AxQmbDyyDQA8fnNI'
OSS_BUCKET_NAME = 'abc-crawler'
OSS_ENDPOINT = 'networks://oss-cn-hangzhou-internal.aliyuncs.com'


class Uploader(object):

    def __init__(self):
        self.bucket = oss2.Bucket(oss2.Auth(OSS_ACCESS_KEY, OSS_ACCESS_KEY_SECRET), OSS_ENDPOINT, OSS_BUCKET_NAME)
        self.logger = logging.getLogger("Uploader")

    def update_file(self, data, filename, progress_callback=None):
        """
        上传pdf文件到阿里云服务器
        :param data: 文件数据
        :param filename: 存储的文件名
        :return:
        """
        headers = {"Content-Type": "application/pdf"}
        try:
            result = self.bucket.put_object(key=filename, data=data, headers=headers,
                                            progress_callback=progress_callback)
            self.logger.info('upload oss result: %s, status : %s', result, result.status)
            if result.status != 200:
                self.logger.error('upload file %s failed with result %s', filename, result.status)
                return False
            else:
                self.logger.info('upload file %s ok, now remove temp file', filename)
                return True
        except Exception as e:
            self.logger.error('upload file %s failed, error %s', filename, e.message)
            return False
    def upload_file(self, oss_path, filename):
        """
        上传pdf文件到阿里云放服务器
        :param oss_path: 文件路径
        :param filename: 存储的文件名
        :return:
        """
        try:
            result = self.bucket.put_object_from_file(oss_path, filename)
            self.logger.info('upload oss result: %s, status : %s', result, result.status)
            if result.status != 200:
                self.logger.error('upload file %s failed with result %s', filename, result.status)
                return False
            else:
                self.logger.info('upload file %s ok, now remove temp file', filename)
                return True
        except Exception as e:
            self.logger.error('upload file %s failed, error %s', filename, e.message)
            return False

if __name__ == '__main__':
    log_path = os.path.join('/', config.configs.get("logfile"), 'uploader.log')
    logging.basicConfig(filename=log_path, format='%(asctime)s %(name)s %(levelname)s: %(message)s',
                        level=logging.DEBUG)
    uploader = Uploader()
    uploader.upload_file('act-ifrs9-jul2016.pdf', 'act-ifrs9-jul2016.pdf')