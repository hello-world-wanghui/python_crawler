#! /usr/bin/env python
# -*- coding: utf-8 -*-

from base.database import *
from configs.logconfig import FinalLogger
from base.Tool import *
import os
from networks import *
import datetime
from configs import config

class job_base():
    """
    这是job基类  爬虫任务可以继承它开发
    """
    def __init__(self, loggingname=None, fmt=None, log_file=None, proxie=None):
        """
        初始化日志文件配置
        """
        self.configs = config.configs
        log_path = self.configs.get("logfile")

        loggingname = loggingname if loggingname else self.__class__.__name__
        fmt = fmt if fmt else '%(asctime)s %(name)s %(levelname)s: %(funcName)s %(lineno)d %(message)s'
        log_file = log_file if log_file else os.path.join(log_path, self.__class__.__name__ + ".log")
        self.logger = FinalLogger().getLogger(loggingname=loggingname, fmt=fmt, log_file=log_file)

    def run(self):
        """
        任务入口 需要重写
        :return:
        """
        pass

    def __run__(self, settings):
        """
        调度程序的入口
        调度框架会直接调用__run__方法
        :param func:
        :return:
        """
        self.settings = settings
        self.gethttp_reques()
        starttime = datetime.datetime.now()
        self.logger.warning("run: " + str(self.__class__.__name__))
        self.run()
        self.__end__(starttime)


    def __end__(self, starttime):
        """
        job程序结束操作
        :param starttime:
        :param func:
        :return:
        """
        self.end()
        self.logger.warning("run: "+str(self.__class__.__name__) + " ok exit")
        self.logger.warning("send networks count: "+self.http.__send_count__.__str__())
        self.logger.warning("error send networks count: "+self.http.__send_error__.__str__())
        self.logger.warning("succeed send networks count: "+self.http.__send_succeed__.__str__())
        self.logger.warning("用时: "+ str((datetime.datetime.now() - starttime).total_seconds()) + "(seconds)")

    def end(self):
        """
        程序结束时自动执行 有需要可以重写
        :return:
        """
        pass

    def getmongoconn(self):
        """
        获取Mongo链接对象
        :return:
        """
        if hasattr(self, "mongoconn"):
            self.logger.warning("mongoconn There are")
            return True
        else:
            mongo = mongoCollection(logger=self.logger)
            self.mongoconn = mongo.mongoconn
            if self.mongoconn:
                return True
            else:
                self.logger.error("链接Mongo出错")
                return False

    def getmongoTool(self):
        if self.getmongoconn():
            mongotool = mongoDBTool(logger=self.logger)
            return mongotool
        else:
            return False

    def getmysqlconn(self):
        """
        获取mysql对象
        :return:
        """
        mysql = mysqlconn(logger=self.logger)
        self.mysqlconn = mysql.getmysqlconn(self.logger)

    def gethttp_reques(self):
        """
        获取发送http请求对象
        :return:
        """
        if not hasattr(self, "http"):
            self.http = http_request(self.logger, self.settings)

    def get_net_Tool(self):
        """
        获取网络工具
        :return:
        """
        net_tool = net_Tool()
        return net_tool

    def Verification(self, imgdata, code):
        """
        验证码识别
        :param imgdata 图片数据
        :param code 解析编码
        :return: dict
        来源超级鹰  具体参考 networks://www.chaojiying.com/price.html
        英文数字
        code	验证码描述	        官方单价(题分)
        1901	    企鹅专用4位英文	        10
        1902	    常见4位英文数字	        10
        1101	    1位英文数字	            10
        1004	    1~4位英文数字	        10
        1005	    1~5位英文数字	        12
        1006	    1~6位英文数字	        15
        1007	    1~7位英文数字	        17.5
        1008	    1~8位英文数字	        20
        1009	    1~9位英文数字	        22.5
        1010	    1~10位英文数字	        25
        1012	    1~12位英文数字	        30
        1020	    1~20位英文数字	        50

        中文汉字
        code	       验证码描述	    官方单价(题分)
        2002	       1~2位纯汉字	         20
        2003	       1~3位纯汉字	         30
        2004	       1~4位纯汉字	         40
        2005	       1~5位纯汉字	         50
        2006	       1~6位纯汉字	         60
        2007	       1~7位纯汉字	         70

        纯数字
        code	       验证码描述	      官方单价(题分)
        4004	       1~4位纯数字	          10
        4005	       1~5位纯数字	          12
        4006	       1~6位纯数字	          15
        4007	       1~7位纯数字	          17.5
        4008	       1~8位纯数字	          20
        4111	       11位纯数字	          25

      任意特殊字符
        code	       验证码描述	                官方单价(题分)
        5000	       不定长汉字英文数字	            2.5每英文，10每汉字 (基础10)
        5108	       8位英文数字(包含字符)	             22
        5201	       拼音首字母，计算题，成语混合，计算20，成语40
        5211	       集装箱号 4位字母7位数字	        30

        """
        chaojiying = Chaojiying_Client()
        return chaojiying.PostPic(imgdata, code)

    def VerificationError(self, im_id):
        """
        识别错误提交
        :param im_id: im_id
        :return:
        """
        chaojiying = Chaojiying_Client()
        chaojiying.ReportError(im_id)

    def send_mail(self, to_list, sub, content):
        """
        发送邮件
        :param to_list: 收件地址
        :param sub:  主题
        :param content: 内容
        :return:
        """
        mail().send_mail(to_list=to_list, sub=sub, content=content)
