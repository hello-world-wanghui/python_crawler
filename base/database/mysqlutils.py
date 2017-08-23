#! /usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
from configs import config

class mysqlconn(object):
    """
    mysql 链接
    """
    def __init__(self, logger, mysqlconf=None):
        self.logger = logger
        self.mysqlconf = config.configs.get("mysql")
        self.mysqlconn = self.getmysqlconn(mysqlconf)

    def getmysqlconn(self, mysqlconf):
        """
        链接mysql数据库
        :param mysqlconf:
        :return:
        """
        if not mysqlconf:
            mysqlconf = self.mysqlconf
        try:
            conn = MySQLdb.connect(**mysqlconf)
            self.logger.info("link mysql :" + str(self.mysqlconf))
            return conn
        except Exception as e:
            self.logger.error("link mysql error : " + e.message)
            return False

class mysqlTool(mysqlconn):
    """
    mysql 工具类
    """

    def mysqlselect(self, sql):
        """
        :param sql: 数据库查询语句
        :return: info：数据库的查询结果 for循环遍历出来
                 mysql数据的查询操作
        #>>> from data import mysqlData
        #>>> from data.Data import mysqlData
        #>>> app=mysqlData()
        #>>> data=app.mysqlselect("select * from tbname")
        #>>> for i in data:
                print i
        """
        try:
            cur = self.mysqlconn.cursor()  # 获取数据库连接对象
            num = cur.execute(sql)  # 上传sql语句
            info = cur.fetchmany(num)
            cur.close()
            self.mysqlconn.commit()
            return info
        except Exception as e:
            self.logger.error("perform sql error : "+e.message)
            self.logger.error("sql: "+str(sql))
            return False

    def mysqlinsert(self, sql):
        """
        mysql插入数据库操作
        :param sql: sql 插入语句
        :return: True False
        """
        try:
            cur = self.mysqlconn.cursor()
            cur.execute(sql)
            cur.close()
            self.mysqlconn.commit()
            return True
        except Exception as e:
            self.logger.error("perform sql error : " + e.message)
            self.logger.error("sql :" + str(sql))
            return False