#coding=utf-8

import json
import uuid
import logging

from utils.contansts import SESSION_EXPIRE_TIME

class Session(object):
    """
    存储用户session  数据缓存在redis
    """
    def __init__(self, request_obj):
        """
        :param request_obj: 用户当前请求的handler
        """

        self._request_handler   = request_obj
        # self._session_id        = request_obj.get_secure_cookie('session_id')
        self._session_id = request_obj.get_argument("token", None)

        if not self._session_id:
            self._session_id = uuid.uuid4().hex
            self.data = {}
            request_obj.set_secure_cookie("session_id", self._session_id)

        else:
            try:
                jsondata = request_obj.redis.get("session_id:%s" % (self._session_id) )
            except Exception as e:
                logging.error(e)
                raise e

            if not self.data:
                self.data = {}
            else:
                self.data = json.loads(jsondata)

    def save(self):
        """
        :return: None
        """

        json_str  = json.dumps(self.data)
        try:
            self._request_handler.redis.set("session_id:%s" % self._session_id, json_str, SESSION_EXPIRE_TIME)
        except Exception as e:
            logging.error(e)
            raise e

    def clear(self):
        """

        :return:
        """
        try:
            self._request_handler.redis.delete("session_id:%s" % self._session_id)
        except Exception as e:
            logging.error(e)
            raise e
        self._request_handler.clear_cookie("session_id")

    def clear_session(self, session_id):
        if not isinstance(session_id, bytes):
            raise TypeError("session_id 不正确")

        try:
            logging.debug("session_id:%s" % session_id.decode('utf8'))
            self._request_handler.redis.delete("session_id:%s" % session_id.decode('utf8'))
        except Exception as e:
            logging.error(e)
            raise e

def main():
    pass


if __name__ == '__main__':
    main()