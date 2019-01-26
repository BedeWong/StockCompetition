#coding=utf-8

from tornado.web import RequestHandler

from utils.session import Session

import json

class BaseHandler(RequestHandler):
    """

    """

    @property
    def redis(self):
        return  self.application.redis

    def prepare(self):
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = {}


    def set_default_headers(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.set_header("Age", "60")

    def get_current_user(self):
        """
        返回当前的登录用户：从redis获取
        :return: data：None 则表示没有数据，未登录
        """
        self.session = Session(self)
        return self.session.data

def main():
    pass


if __name__ == '__main__':
    main()