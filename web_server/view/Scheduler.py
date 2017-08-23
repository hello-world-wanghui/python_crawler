#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
from tornado import web
from Scheduling.Scheduling_start import Scheduling_start

class Scheduler_start(web.RequestHandler):
    """
    启动 调用器
    """
    def get(self, *args, **kwargs):
        if self.settings.get("Scheduler").Background.running:
            self.write(json.dumps({"errcode": "0", "message": "Scheduler is alerady running"}))
        else:
            try:
                self.settings.get("Scheduler").Background.start()
                self.write(json.dumps({"errcode": "0", "message": "start Scheduler"}))
            except Exception as e:
                self.write(json.dumps({"errcode": "500", "message": "start Scheduler error: " + e.message}))

class Scheduler_status(web.RequestHandler):
    """
    查看调度器状态
    """
    def get(self, *args, **kwargs):
        try:
            status = self.settings.get("Scheduler").Background.running
            self.write(json.dumps({"errcode": "0", "status": status.__str__()}))
        except Exception as e:
            self.write(json.dumps({"errcode": "500", "message": "select Scheduler status error:" + e.message}))


class Scheduler_shutdown(web.RequestHandler):
    """
    停止调度器
    """
    def get(self, *args, **kwargs):
        if self.settings.get("Scheduler").Background.running:
            try:
                self.settings.get("Scheduler").Background.shutdown()
                self.write(json.dumps({"errcode": "0"}))
            except Exception as e:
                self.write(json.dumps({"errcode": "500", "message": "shutdown Scheduler error:" + e.message}))
        else:
            self.write(json.dumps({"errcode": "4001", "message": "Scheduler is alerady shutdown"}))

class Select_jobs(web.RequestHandler):
    """
    获取所有job
    """
    def get(self, *args, **kwargs):
        try:
            jobs = self.settings.get("Scheduler").Background.get_jobs()
            data = dict()
            datalist = list()
            for i in jobs:
                datalist.append({
                    "job_id": str(i.id),
                    "project_name": str(i.executor),
                    "next_run_time": str(i.next_run_time),
                    "start_date": str(i.trigger.start_date)
                })
            data["data"] = datalist
            data["errcode"] = "0"
            self.write(json.dumps(data))
        except Exception as e:
            self.write(json.dumps({"errcode": "500", "message": "get jobs error" + e.message}))

class add_job(web.RequestHandler):
    """
    添加一个任务
    """
    def get(self, *args, **kwargs):
        trigger_args = dict()
        try:
            trigger_args["job_path"] = self.get_argument("job_path")
            trigger_args["classname"] = self.get_argument("classname")
            trigger_args["job_id"] = self.get_argument("job_id")
            trigger_args["trigger"] = self.get_argument("trigger")
        except Exception:
            self.write(json.dumps({"errcode": "4002", "message": "The required parameters are not provided"}))
            self.finish()
            return
        trigger_args["args"] = self.get_argument("args", "").split()
        trigger_args["name"] = self.get_argument("name", trigger_args['job_id'])
        trigger_args["jobstore"] = self.get_argument("jobstore", "default")
        key = self.get_argument("key", "").split()
        value = self.get_argument("value", "").split()
        for i in range(key.__len__()):
            trigger_args[key[i]] = value[i]
            if key[i] in ["weeks", "days", "hours", "minutes", "seconds"]:
                try:
                    trigger_args[key[i]] = int(value[i])
                except Exception:
                    self.write(json.dumps({"errcode": "4002", "message": str(key[i]) + ": You need an int"}))
        trigger_args["job_path"] = "job.crawler_job."+trigger_args["job_path"]
        Scheduler = self.settings.get("Scheduler")
        if isinstance(Scheduler, Scheduling_start):
            try:
                if Scheduler.Background.running:
                    message = Scheduler.add_job(**trigger_args)
                    self.write(json.dumps({"errcode": "0", "message": message.__str__()}))
                else:
                    self.write(json.dumps({"errcode": "4005", "message": "cannot schedule new futures after shutdown"}))
            except Exception as e:
                self.write(json.dumps({"errcode": "4001", "message": e.message}))

class Schedule_delete_job(web.RequestHandler):
    """
    删除一个 任务
    """
    def get(self, *args, **kwargs):
        job_ID = self.get_argument("jobID")
        try:
            self.settings.get("Scheduler").Background.remove_job(job_id=job_ID)
            self.write(json.dumps({"errcode": "0", "message": "delete job " + job_ID}))
        except Exception as e:
            self.write(json.dumps({"errcode": "4001", "message": e.message}))

class Schedule_delete_all_job(web.RequestHandler):
    """
    删除所有任务
    """
    def get(self, *args, **kwargs):
        Scheduler = self.settings.get("Scheduler")
        jobstore = self.get_argument("jobstore", None)
        if isinstance(Scheduler, Scheduling_start):
            try:
                job_Id = Scheduler.Background.remove_all_jobs(jobstore=jobstore)
                self.write(json.dumps({"errcode": "0", "message": job_Id}))
            except Exception as e:
                self.write(json.dumps({"errcode": "4001", "message": e.message}))

class Schedule_pause(web.RequestHandler):
    """
    暂停调度器
    """
    def get(self, *args, **kwargs):
        try:
            Scheduler = self.settings.get("Scheduler").Background
            Scheduler.pause()
            self.write(json.dumps({"errcode": "0"}))
        except Exception as e:
            self.write(json.dumps({"errcode": "4001", "message": e.message}))

class Schedule_resume(web.RequestHandler):
    """
    恢复调度器
    """
    def get(self, *args, **kwargs):
        try:
            Schedule = self.settings.get("Scheduler").Background
            Schedule.resume()
            self.write(json.dumps({"errcode": "0"}))
        except Exception as e:
            self.write(json.dumps({"errcode": "4001", "message": " resume Schedule error :" + e.message}))

class Schedule_modify_job(web.RequestHandler):
    """
    修改任务
    """
    def get(self, *args, **kwargs):
        changes = dict()
        for i in self.request.arguments:
            changes[i] = self.get_argument(i)
        if not changes["job_id"]:
            self.write(json.dumps({"errcode": "4002", "message": "modify job error : not job_id"}))
            self.finish()
        try:
            Schedule = self.settings.get("Scheduler").Background
            message = Schedule.modify_job()
            json.dumps({"errcode": "0", "message": message})
            self.write(message)
        except Exception as e:
            json.dumps({"errcode": "4001", "message": "modify job error : " + e.message})

class Schedule_pause_job(web.RequestHandler):
    """
    暂停任务
    """
    def get(self, *args, **kwargs):
        job_ID = self.get_argument("jobID")
        try:
            Schedule = self.settings.get("Scheduler").Background
            message = Schedule.pause_job(job_ID)
            json.dumps({"errcode": "0", "message": message})
        except Exception as e:
            json.dumps({"errcode": "4001", "message": "pause job error: " + e.message})

class Schedule_resume_job(web.RequestHandler):
    """
    恢复任务
    """
    def get(self, *args, **kwargs):
        job_ID = self.get_argument("jobID")
        try:
            Schedule = self.settings.get("Scheduler").Background
            message = Schedule.resume_job(job_ID)
            json.dumps({"errcode": "0", "message": message})
        except Exception as e:
            json.dumps({"errcode": "4001", "message": "pause job error: " + e.message})

urls = [
    ("/Scheduler/start", Scheduler_start),
    ("/Scheduler/status", Scheduler_status),
    ("/Scheduler/shutdown", Scheduler_shutdown),
    ("/Job/get_jobs", Select_jobs),
    ("/Job/add_job", add_job),
    ("/Job/delete_job", Schedule_delete_job),
    ("/Job/delete_all_job", Schedule_delete_all_job),
    ("/Scheduler/pause", Schedule_pause),
    ("/Scheduler/resume", Schedule_resume),
    ("/Job/modify_job", Schedule_modify_job),
    ("/Job/pause_job", Schedule_pause_job),
    ("/Job/resume_job", Schedule_resume_job)
]
