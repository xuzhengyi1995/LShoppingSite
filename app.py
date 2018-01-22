# Main function of app
# XUZhengyi, LIUZijian 22/01/2018

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.log

# Import handlers
from handlers.BasicHandler import BasicHandler

from tornado.options import define, options
define("port", default=80, help="Listen on port", type=int)


class MainApp(tornado.web.Application):

    def __init__(self):
        handlersList = [
            (r"/([^/]+)", BasicHandler)
        ]
        tornado.web.Application.__init__(self, handlersList)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    mainApp = MainApp()
    http_server = tornado.httpserver.HTTPServer(mainApp)
    http_server.listen(options.port)
    print('Start listing on port:', options.port)
    tornado.ioloop.IOLoop.instance().start()
