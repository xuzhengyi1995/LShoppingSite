# BasicHandlers.py
# XUZhengyi, 22/01/2018

import tornado.web


class BasicHandler(tornado.web.RequestHandler):
    def get(self, parm):
        res = "This is test for BasicHandlers. Parm = " + parm
        self.write(res)
