#! /usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from job.job_base import job_base

class peoxie1(job_base):
    """
    付费代理获取
    """
    def get_proxies(self):
        proxies = []
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Host': 'nc-11.f3322.net:1022',
            'Referer': 'http://nc-11.f3322.net:1022/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
        }
        url = 'http://nc-11.f3322.net:1022/login.php'
        data = {
            'username': 'abcdft123',
            'password': 'abcdft123@920928',
            'submit': '++确+定++'
        }
        self.logger.info("send peoxies ip: " + str(url))
        res = self.http.send_http(method="post", url=url, data=data, isproxie=False, headers=headers)
        html = res.content.decode('utf8')
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        s = soup.select('pre')[0].get_text()
        ps = s.split('\r\n')
        for line in ps:
            ip, port, user, pwd = [val.strip() for val in line.split(':')]
            proxy = {'http': 'http://%s:%s@%s:%s' % (user, pwd, ip, port)}
            proxies.append(proxy)
        self.logger.info("The proxy IP" + str(proxies))
        return proxies

    def run(self):
        proxies = self.get_proxies()
        self.settings["proxies"] = proxies