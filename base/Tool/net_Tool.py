#! /usr/bin/env python
# -*- coding: utf-8 -*-

import StringIO
import gzip
import re
import platform
if "Windows" in platform.system():
    from Cryptodome.Cipher import PKCS1_v1_5
    from Cryptodome.PublicKey import RSA
if "Linux" in platform.system():
    from Crypto.Cipher import PKCS1_v1_5
    from Crypto.PublicKey import RSA
import base64

class net_Tool():

    def __init__(self):
        pass

    def decode_html(self,html):
        """
        解码gzip页面
        :return:
        """
        compressedstream = StringIO.StringIO(html)
        gzipper = gzip.GzipFile(fileobj=compressedstream)
        data = gzipper.read()
        return data

    def deleteSpace(self, text):
        """
        清除所有的空格回车tab
        :return:
        """
        return re.sub('\s|&nbsp|\xa0|\\xa0|\u3000|\\u3000|\\u0020|\u0020', "", unicode(text))

    def urltohttp(self, url, host):
        """
        拼接host和url
        :param url:
        :param host:
        :return:
        """
        if "networks" in url:
            return url
        else:
            return host + url

    def extracthttp(self, string):
        """
        正则匹配url
        :return:
        """
        return re.findall("(htt[ps]+://[A-Za-z.0-9/&?=\-]+)", string)

    def RSA(self, key_bytes, message):
        """
        rsa加密
        :return:
        """
        if 'BEGIN PUBLIC KEY' not in key_bytes:
            key_bytes = '-----BEGIN PUBLIC KEY-----\n' + key_bytes + '\n-----END PUBLIC KEY-----'
        key_bytes = key_bytes.replace('\\n', '\n').replace('\\', '')
        rsakey = RSA.importKey(key_bytes)
        cipher = PKCS1_v1_5.new(rsakey)
        password = base64.b64encode(cipher.encrypt(message))
        return password