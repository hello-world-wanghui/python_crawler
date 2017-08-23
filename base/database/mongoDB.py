#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from configs import config
import pymongo
import logging
import sys

class mongoCollection(object):
    """
    连接mongo类
    """
    def __init__(self, logger, url=None, db=None):
        self.mongoconf = config.configs.get("mongo")
        self.mongoconn = self.Mongoconn()
        self.logger = logger

    def Mongoconn(self, url=None, db=None):
        if url and db:
            try:
                mongo_db = pymongo.MongoClient(url)[db]
            except EOFError as e:
                logging.error(e)
                return False
        else:
            try:
                mongo_db = pymongo.MongoClient(self.mongoconf.get("MONGO_URI")
                                               )[self.mongoconf.get('MONGO_DB')]
            except EOFError as e:
                logging.error(e)
                return False
        return mongo_db

class mongoDBTool(mongoCollection):
    """
    mongodb tool
    """

    def save_mongodb(self, data, find, tablename):
        """
        检查key值是否存在 存在则更新 不存在则插入
        :param data : 需要插入的数据 dict
        :param find : 匹配的字段 dict
        tablename: 相关表
        :return:
        """
        MovieID = getattr(self.mongoconn, tablename).find(find)
        if MovieID.count():
            getattr(self.mongoconn, tablename).update(find, {'$set': data})
        else:
            getattr(self.mongoconn, tablename).insert(data)

    def select(self, tablename, find):
        return getattr(self.mongoconn, tablename).find(find)
