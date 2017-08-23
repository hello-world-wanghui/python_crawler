#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from Scheduling.Scheduling_start import Scheduling_start
from tornado import web, ioloop
import logging
import os
from configs import config
import web_server

reload(sys)
sys.setdefaultencoding('utf-8')

class web_start():
    def __init__(self):
        self.configs = config.configs
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%Y/%m/%d %H:%M:%S',
                            filename=os.path.join(self.configs.get("logfile"), 'web_server.log'),
                            filemode='w')
        self.logger = logging

    def web_app(self):
        Scheduler = Scheduling_start(self.logger)
        settings = dict(
            Scheduler=Scheduler,
            template_path=os.path.join(os.path.dirname(__file__), "web_server\\template"),
            static_path=os.path.join(os.path.dirname(__file__), "web_server\\static"),
            static_url_prefix='/static/'
        )
        return web.Application(handlers=web_server.urlheaders, **settings)

if __name__ == "__main__":
    app = web_start()
    tornado_app = app.web_app()
    tornado_app.listen(9264)
    ioloop.IOLoop.current().start()