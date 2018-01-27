# Main function of app
# XUZhengyi, LIUZijian 22/01/2018

import os
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.log
from common.Db import Db

# Import handlers
from handlers.BasicHandler import BasicHandler
from handlers.IndexHandler import IndexHandler
from handlers.SearchHandler import SearchHandler
from handlers.GetProductHandler import GetProductHandler
from handlers.AuthHandlers import LoginHandler

# Import moudles
from moudles.OneProductMoudle import OneProductMoudle
from moudles.SortPageMoudle import SortPageMoudle

from tornado.options import define, options
define("port", default=80, help="Listen on port", type=int)


class MainApp(tornado.web.Application):

    def __init__(self, db, _debug=False):
        handlersList = [
            (r"/", IndexHandler),
            (r"/search", SearchHandler),
            (r"/product/(https?://[^/]+)/([^/]+)/?", GetProductHandler),
            (r"/login", LoginHandler),
            (r"/.*", BasicHandler)
        ]
        modulesList = {
            'OneProduct': OneProductMoudle,
            'SortPageBar': SortPageMoudle
        }
        tpath = os.path.join(os.path.dirname(__file__), "templates")
        spath = os.path.join(os.path.dirname(__file__), "static")

        settings = {
            'template_path': tpath,
            'static_path': spath,
            'ui_modules': modulesList,
            'debug': _debug,
            'cookie_secret': 'E1ov3DpQT82nNHIV3bUJPShp4pw+Qka4kQW3fjervd4=',
            "xsrf_cookies": True
        }
        self.db = db
        tornado.web.Application.__init__(self, handlersList, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    mainApp = MainApp(Db(), True)
    http_server = tornado.httpserver.HTTPServer(mainApp)
    http_server.listen(options.port)
    print('Start listing on port:', options.port)
    tornado.ioloop.IOLoop.instance().start()
