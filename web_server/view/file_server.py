#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from base.Tool.commontools import commontools
from tornado import web, httpserver, ioloop, gen
url = "/file/"


class FileUploadHandler(web.RequestHandler):

    def get(self, *args, **kwargs):
        self.write('''
        <html>
          <head><title>Upload File</title></head>
          <body>
            <form action='upfile' enctype="multipart/form-data" method='post'>
            <input type='file' name='file'/><br/>
            <input type='submit' value='submit'/>
            </form>
          </body>
        </html>
        ''')

    def post(self, *args, **kwargs):
        tool = commontools()
        ret = {"result": "ok"}
        upload_path = os.path.join(os.path.dirname(__file__), "file")
        file_meatas = self.request.files.get("file", None)
        if not file_meatas:
            ret["result"] = "Invalid Args"
            return ret
        for meta in file_meatas:
            filename = meta['filename']
            tool.writefile(file_url=upload_path, filename=filename, filedata=meta['body'])
        self.write(json.dumps(ret))

urls = [
    (url + "upload", FileUploadHandler),
]