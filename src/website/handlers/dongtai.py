#coding=utf-8
import logging
from utils.commons import required_login

from utils.response_code import RET, RETMSG_MAP
from handlers.basehandler import BaseHandler
from handlers.services.svc_dongtai import SVC_Dongtai

class GetDongTaiByUid(BaseHandler):
    """
    獲取用戶的動態數據， 指的是這一個用戶的動態
    """

    @required_login
    def get(self, *args, **kwargs):
        """
        userid:
        page:
        count:
        :return:
        """

        uid = self.get_argument("userid")
        page = (int)(self.get_argument("page", 0))
        count = (int)(self.get_argument("count", 40))

        res = None
        try:
            res = SVC_Dongtai.get_dongtai_by_uid(uid, page, count)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            return

        if not res:
            res = []

        self.write(dict(
            errcode=RET.RET_OK,
            errmsg="",
            retdata = res
        ))


class getDongTaiByUser(BaseHandler):
    """
    獲取用戶的動態，獲取的是這個用戶的動態和他關注的人的動態
    """

    @required_login
    def get(self, *args, **kwargs):
        """
        userid:
        page：
        count:
        :return:
        """

        uid = self.get_argument("userid")
        page = (int)(self.get_argument("page", 0))
        count = (int)(self.get_argument("count", 40))

        res = None
        try:
            res = SVC_Dongtai.get_dongtai_by_user(uid, page, count)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            return

        if not res:
            res = []

        self.write(dict(
            errcode = RET.RET_OK,
            errmsg = "",
            retdata = res
        ))


def main():
    pass


if __name__ == '__main__':
    main()