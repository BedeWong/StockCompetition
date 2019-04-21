#coding=utf-8

import logging

import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver

import redis
import os
import sys
import config

from tornado.options import options, define
from tornado.web import RequestHandler

from urls import urls

define("port", default=8001, type=int, help="程序运行在这个端口")
# define("logging", default="debug", help="日志默认等级")
# define("log_file_max_size", type=int, default=100 * 1000 * 1000,
#                    help="max size of log files before rollover")
# define("log_file_num_backups", type=int, default=5,
#                    help="number of log files to keep")
# define("log_rotate_when", type=str, default='midnight',
#                help=("specify the type of TimedRotatingFileHandler interval "
#                      "other options:('S', 'M', 'H', 'D', 'W0'-'W6')"))

class Application(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.redis = redis.StrictRedis(**config.redis_opt)


def main():
    options.logging = 'debug'
    options.log_file_max_size = 100 * 1000 * 1000
    options.log_file_num_backups = 5
    options.log_rotate_when = 'midnight'

    tornado.options.parse_command_line()	

    app = Application(
        urls,
        **config.settings
    )
    server = tornado.httpserver.HTTPServer(app)
    
    # options.log_file_prefix = config.log_path + "_" + (str)(options.port)
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
