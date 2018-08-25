#coding=utf-8
import logging
from utils.commons import required_login

from utils.response_code import RET, RETMSG_MAP
from handlers.basehandler import BaseHandler
from handlers.services.svc_article import SVC_Article
from handlers.services.svc_dongtai import SVC_Dongtai

class addArticle(BaseHandler):
    """
    用戶發表一個話題
    """
    @required_login
    def post(self, *args, **kwargs):
        """
        uid:
        title:
        content:
        :return:
        """

        uid = self.get_argument("uid")
        title = self.get_argument("title")
        content = self.get_argument("content")

        try:
            aid =  SVC_Article.addArticle(uid, title, content)
            SVC_Dongtai.add_dongtai_pub_topic(uid, aid, title)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode = RET.RET_SERVERERR,
                errmsg = RETMSG_MAP[RET.RET_SERVERERR]
            ))
            raise e

        self.write(dict(
            errcode = RET.RET_OK,
            errmsg = ""
        ))


class delArticle(BaseHandler):
    """
    刪除一個話題， 需要檢測用戶id是否匹配
    """

    @required_login
    def post(self, *args, **kwargs):
        """
        uid:
        aid:
        :return:
        """

        uid = self.get_argument("uid")
        aid = self.get_argument("aid")

        try:
            SVC_Article.delArticle(uid, aid)
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

class getArticleById(BaseHandler):
    """
    根據id獲取話題詳情：
    """
    @required_login
    def get(self, *args, **kwargs):
        """
        id；話題id
        :return:
        """

        aid = self.get_argument("aid")
        res = None
        try:
            res = SVC_Article.getArticleById(aid)
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

class getArtilceByUid(BaseHandler):
    """
    獲取一個用戶發表的話題
    """

    @required_login
    def get(self, *args, **kwargs):
        """

        :return:
        """

        uid = self.get_argument("uid")
        page = (int)(self.get_argument("page", 0))
        count = (int)(self.get_argument("count", 40))
        res = None
        try:
            res = SVC_Article.getArticleByUid(uid, page, count)
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

class getNewestArticle(BaseHandler):
    """
    獲取最新的文章
    """

    @required_login
    def get(self, *args, **kwargs):
        """

        :return:
        """

        page = (int)(self.get_argument("page", 0))
        count = (int)(self.get_argument("count", 40))
        res = None
        try:
            res = SVC_Article.getNewestArticles(page, count)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            raise e

        self.write(dict(
            errcode = RET.RET_OK,
            errmsg = "",
            retdata = res
        ))

class getHotArticle(BaseHandler):
    """
    獲取熱門的話題
    """

    @required_login
    def get(self, *args, **kwargs):
        """
        獲取熱話題
        :return:
        """

        latest = self.get_argument("latest")
        page = self.get_argument("page", 0)
        count = self.get_argument("count", 40)

        res = None
        try:
            res = SVC_Article.getArticleNewestHot(latest, page, count)
        except Exception as e:
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            raise e

        self.write(dict(
                    errcode = RET.RET_OK,
                    errmsg = "",
                    retdata = res
        ))

class checkUpcount(BaseHandler):
    """

    """
    @required_login
    def get(self, *args, **kwargs):
        """

        :return:
        """

        uid = self.get_argument("uid")
        aid  = self.get_argument("aid")

        res = False
        try:
            res = SVC_Article.checkUpcount(uid, aid)
        except Exception as e:
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            raise e

        self.write(dict(
            errcode = RET.RET_OK,
            errmsg = "",
            retdata = res
        ))

class UpcountArticle(BaseHandler):
    """
    給文章點贊, 點過的就取消了
    """
    @required_login
    def post(self, *args, **kwargs):
        """
        uid：
        aid:
        :return:
        """

        uid = self.get_argument("uid")
        aid = self.get_argument("aid")
        try:
            SVC_Article.upcountArticle(aid, uid)
        except Exception as e:
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            raise e

        self.write(dict(
            errcode = RET.RET_OK,
            errmsg = ""
        ))

def main():
    pass


if __name__ == '__main__':
    main()