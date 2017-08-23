#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests
from base.Tool import *

class http_request(object):
    """
    http请求类
    """
    default_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "Content-type": "application/json"
    }

    def __init__(self, logger, settings):
        self.client = requests.session()
        self.logger = logger
        self.__send_count__ = 0
        self.__send_error__ = 0
        self.__send_succeed__ = 0
        self.index = 0
        self._proxies = settings.get("proxies", [])

    def __proxie_send(self, method, url, **kwargs):
        """
        使用代理发送http请求
        :param method: 请求方式
        :param url: 请求url
        :param kwargs:
        :return:
        """
        proxies = self.get_proxie()
        if proxies:
            self.logger.info("proxie:" + proxies.__str__())
            kwargs["proxies"] = proxies
        else:
            self.logger.warning("not proxie Replace local IP")
        return self.__local_send(method=method, url=url, **kwargs)

    def __local_send(self, method, url, **kwargs):
        """
        使用本地ip发送http请求
        :param method: 请求方式
        :param url: 请求url
        :param kwargs:
        :return:
        """
        self.__send_count__ += 1
        try:
            res = self.client.request(method=method, url=url, **kwargs)
            self.__send_succeed__ += 1
            return res
        except Exception as e:
            self.logger.error("send url error: "+e.message+" url: "+url)
            self.__send_error__ += 1
            return False

    def start_http(self, **kwargs):
        """
        http请求前操作
        :return:
        """
        return kwargs

    def end_http(self, args):
        """
        http请求完成操作
        :param kwargs:
        :return:
        """
        return args

    def send_http(self, method, url, sleep=5, isproxie=False, **kwargs):
        """
        http请求入口
        :param method: 请求方式
        :param url: 请求url
        :param sleep: 休眠时间
        :param isproxie: 是否使用代理
        :param kwargs:
        :return:
        """
        send_count = 0
        #固定休眠 防止请求过快
        time.sleep(sleep)
        httpdic = self.start_http(method=method, url=url, **kwargs)
        kwargs["verify"] = False
        while True:
            send_count += 1
            if isproxie:
                res = self.__proxie_send(**httpdic)
            else:
                res = self.__local_send(**httpdic)
            if res:
                return self.end_http(res)
            elif send_count > 4:
                baidu = self.__local_send(method=method, url="https://www.baidu.com", **kwargs)
                if not baidu:
                    mail().send_mail(to_list=["13264616071@163.com"], sub="http_request",
                                     content="多次出错 请检查代理IP 或者url是否正常")
                return False

    def get_proxie(self):
        """
        获取一个代理
        :return:
        """
        self.index += 1
        try:
            return self.proxies[(self.index % self.proxies.__len__())]
        except Exception as e:
            self.logger.error("get proxie error ")
            self.logger.error(e.message)
            return False

    @property
    def proxies(self):
        return self._proxies

    @proxies.setter
    def proxies(self, value):
        if isinstance(value, list):
            self._proxies.extend(value)
        else:
            self._proxies.append(value)
