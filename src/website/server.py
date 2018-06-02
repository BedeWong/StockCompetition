#coding=utf-8

import logging

import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver

import redis
import os
import config

from tornado.options import options, define
from tornado.web import RequestHandler

from urls import urls

define("port", default=8001, type=int, help="程序运行在这个端口")

class Application(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.redis = redis.StrictRedis(**config.redis_opt)


def main():
    options.log_file_prefix = config.log_path
    options.logging = config.log_level

    tornado.options.parse_command_line()

    app = Application(
        urls,
        **config.settings
    )
    server = tornado.httpserver.HTTPServer(app)
    logging.debug(options.port)
    server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()