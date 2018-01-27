# IndexHandler
# XUZhengyi, 23/01/2018

import tornado.web
from handlers.BasicHandler import BasicHandler


class IndexHandler(BasicHandler):
    def get(self):
        self.render('index.html', info=self.info)
