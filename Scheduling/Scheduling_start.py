#! /usr/bin/env python
# -*- coding: utf-8 -*-

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.events import EVENT_JOB_ERROR
from base.Tool.send_mail import mail

class Scheduling_start():
    """
    启动 Scheduling
    """
    def __init__(self, logger):
        self.settings = dict()
        self.logger = logger
        self.start_Scheduling()

    def start_Scheduling(self):
        executors = {
            'default': ThreadPoolExecutor(20),
            'processpool': ProcessPoolExecutor(3)
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': 10
        }

        self.Background = BackgroundScheduler(executors=executors,
                                              job_defaults=job_defaults)
        self.logger.info("start Scheduler")
        self.Background.start()
        self.Background.add_listener(self.JOB_ERROR, mask=EVENT_JOB_ERROR)

    def add_job(self, job_path, classname, job_id, trigger, args=None, **trigger_args):
        """
        这是定时任务列表 每一个带有sched.scheduled_job()装饰器的函数都是一个定时任务
        你可以添加这样的函数给你的程序添加定时任务
        trigger =
            date 一次性指定日期
            interval 在某个时间范围内间隔多长时间执行一次
            cron 和Linux crontab格式兼容，最为强大

        date 最基本的一种调度，作业只会执行一次。它的参数如下：
            run_date (datetime|str) – 作业的运行日期或时间
            timezone (datetime.tzinfo|str) – 指定时区

        interval 间隔调度，参数如下：
            默认为1秒钟执行一次
            weeks (int) – 间隔几周
            days (int) – 间隔几天
            hours (int) – 间隔几小时
            minutes (int) – 间隔几分钟
            seconds (int) – 间隔多少秒
            start_date (datetime|str) – 开始日期
            end_date (datetime|str) – 结束日期
            timezone (datetime.tzinfo|str) – 时区

        cron参数如下：
            year (int|str) – 年，4位数字
            month (int|str) – 月 (范围1-12)
            day (int|str) – 日 (范围1-31)
            week (int|str) – 周 (范围1-53)
            day_of_week (int|str) – 周内第几天或者星期几 (范围0-6 或者 mon,tue,wed,thu,fri,sat,sun)
            hour (int|str) – 时 (范围0-23)
            minute (int|str) – 分 (范围0-59)
            second (int|str) – 秒 (范围0-59)
            start_date (datetime|str) – 最早开始日期(包含)
            end_date (datetime|str) – 最晚结束时间(包含)
            timezone (datetime.tzinfo|str) – 指定时区
            取值格式
            表达式	    参数	    描述
            *	        any	        Fire on every value
            */a	        any	        Fire every a values, starting from the minimum
            a-b	        any	        Fire on any value within the a-b range (a must be smaller than b)
            a-b/c	    any	        Fire every c values within the a-b range
            xth y	    day	        Fire on the x -th occurrence of weekday y within the month
            last x	    day	        Fire on the last occurrence of weekday x within the month
            last	    day	        Fire on the last day within the month
            x,y,z	    any	        Fire on any matching expression; can combine any number of any of the above expressions
        """
        if not args:
            args = list()
        args.append(self.settings)
        name = __import__(name=job_path, fromlist=classname)
        funcname = getattr(name, classname)()
        return self.Background.add_job(func=funcname.__run__, trigger=trigger, args=args,
                                id=job_id, **trigger_args)

    def JOB_ERROR(self, event, to_mail="13264616071@163.com"):
        """
        job 异常监听
        :param event:
        :param to_mail:
        :return:
        """
        if not isinstance(to_mail, list):
            to_mail = [to_mail]
        sub = "crawler job_id:"+str(event.job_id)+" Error"
        content = ("run time: "+event.scheduled_run_time.__str__()+"\n" +
                   "jobstore: "+event.jobstore.__str__()+"\n" +
                   "job_id: "+event.job_id.__str__()+"\n" +
                   "message: "+event.exception.__str__())
        if event.exception:
            self.logger.error("job: "+event.job_id.__str__()+" Error send mail to " + to_mail.__str__())
            mail().send_mail(to_list=to_mail, sub=sub, content=content)
