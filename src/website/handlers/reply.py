#coding=utf-8
import logging
from utils.commons import required_login

from utils.response_code import RET, RETMSG_MAP
from handlers.basehandler import BaseHandler
from handlers.services.svc_reply import SVC_Reply
from handlers.services.svc_dongtai import SVC_Dongtai


#查看是否已經點贊了
class checkUpcount(BaseHandler):
    """
    檢查是否點贊
    """
    @required_login
    def get(self, *args, **kwargs):
        """
        uid:
        rid:
        :return:
        """

        uid = self.get_argument("uid")
        rid = (int)(self.get_argument("rid"))

        res = False
        try:
            res = SVC_Reply.checkUpcount(uid, rid)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            raise e

        self.write(dict(
            errcode=RET.RET_OK,
            errmsg="",
            retdata = res
        ))


class getNewestReply(BaseHandler):
    """
    獲取最新的回復消息
    """

    @required_login
    def get(self, *args, **kwargs):
        """
        ]
        :return:
        """

        page = self.get_argument("page", 0)
        count = self.get_argument("count", 40)

        res = None
        try:
            res = SVC_Reply.getNewestReply(page, count)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            raise e

        self.write(dict(
            errcode=RET.RET_OK,
            errmsg="",
            retdata=res
        ))


class getArticleReplys(BaseHandler):
    """
    獲取一個話題的評論，按頁加載
    """

    @required_login
    def get(self, *args, **kwargs):
        """

        :return:
        """

        aid = (int)(self.get_argument("aid"))
        page = (int)(self.get_argument("page", 0))
        count = (int)(self.get_argument("count", 40))

        res = None
        try:
            res = SVC_Reply.getReplyByArticleId(aid, page, count)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            raise e

        self.write(dict(
            errcode=RET.RET_OK,
            errmsg="",
            retdata=res
        ))


class addReplyReply(BaseHandler):
    """
    評論一個評論
    """

    @required_login
    def post(self, *args, **kwargs):
        """

        :return:
        """

        uid = self.get_argument("uid")
        aid = (int)(self.get_argument("aid"))
        rid = (int)(self.get_argument("rid"))
        content = self.get_argument("content")

        try:
            SVC_Reply.addReplyReply(uid, aid, rid, content)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            raise e

        self.write(dict(
            errcode=RET.RET_OK,
            errmsg=""
        ))


class addReply(BaseHandler):
    """
    給話題天加一個評論
    """

    @required_login
    def post(self, *args, **kwargs):
        """
        uid：
        aid:
        content:
        :return:
        """

        uid = self.get_argument("uid")
        aid = (int)(self.get_argument("aid"))
        content = self.get_argument('content')

        res = None
        try:
            rid = SVC_Reply.addReply(uid, aid, content)
            SVC_Dongtai.add_dongtai_reply(uid, rid, content)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            raise e

        self.write(dict(
            errcode=RET.RET_OK,
            errmsg=""
        ))

class delReply(BaseHandler):
    """
    刪除一個評論
    """
    @required_login
    def post(self, *args, **kwargs):
        """

        :return:
        """

        uid  = self.get_argument("uid")
        # aid = self.get_argument("aid")
        rid = (int)(self.get_argument("rid"))

        try:
            SVC_Reply.delReply(uid, rid)
        except Exception as e:
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            raise e

        self.write(dict(
            errcode=RET.RET_OK,
            errmsg=""
        ))

class upcountReply(BaseHandler):
    """
    給評論點贊
    """

    @required_login
    def post(self, *args, **kwargs):
        """
        點了的就取消點贊
        :return:
        """
        uid = self.get_argument('uid')
        aid = (int)(self.get_argument("aid"))
        rid = (int)(self.get_argument("rid"))
        try:
            SVC_Reply.upcountReply(uid, rid)
        except Exception as e:
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            raise e

        self.write(dict(
            errcode=RET.RET_OK,
            errmsg=""
        ))

def main():
    pass


if __name__ == '__main__':
    main()