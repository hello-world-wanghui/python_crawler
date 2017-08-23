# -*- coding: utf-8 -*-

import logging
from email.mime.text import MIMEText
import smtplib

class mail():
    """
    163 邮件发送
    """
    mail_host = "smtp.163.com" # 邮件服务器
    mail_user = "13264616071@163.com" #发件账户
    mail_pass = "wh123456"  # 邮箱密码

    def __init__(self, host=mail_host, user=mail_user, password=mail_pass):
        """
        :param host: 邮件服务器
        :param user: 发件账户
        :param password: 密码
        """
        self.mail_host = host
        self.mail_user = user
        self.mail_pass = password

    def send_mail(self, to_list, sub, content):
        """
        :param to_list: 收件地址
        :param sub: 邮件主题
        :param content: 邮件内容
        :return:
        """
        me = self.mail_user
        msg = MIMEText(content, _subtype='plain', _charset='utf-8')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            server = smtplib.SMTP()
            server.connect(self.mail_host)
            server.login(self.mail_user, self.mail_pass)
            server.sendmail(me, to_list, msg.as_string())
            server.close()
            return True
        except Exception as e:
            logging.warning(e)
            return False