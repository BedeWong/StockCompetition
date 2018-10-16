#coding=utf-8
import logging
from utils.commons import required_login

from utils.response_code import RET, RETMSG_MAP
from handlers.basehandler import BaseHandler
from handlers.services.svc_article import SVC_Article
from handlers.services.svc_dongtai import SVC_Dongtai
from handlers.services.svc_user_follower import SVC_UserFollower

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
        aid = (int)(self.get_argument("aid"))

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

        aid = (int)(self.get_argument("aid"))
        uid = (int)(self.get_argument("uid"))

        # 獲取文章數據
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

        # 獲取文章作者是不是 本請求的用戶 所關注的
        check = False
        try:
            check = SVC_UserFollower.check_user_folower_relation(res.uid, uid)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            raise e

        # 填寫粉絲關係數據
        res['follower'] = check

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

        latest = (int)(self.get_argument("latest", 7))
        page = (int)(self.get_argument("page", 0))
        count = (int)(self.get_argument("count", 40))

        # 獲取熱門數據
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
        aid  = (int)(self.get_argument("aid"))

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

        uid = (int)(self.get_argument("uid"))
        aid = (int)(self.get_argument("aid"))
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


class UpcountArticleOnly(BaseHandler):
    """
    給文章點贊， 已經點過則點贊失敗
    """

    def post(self, *args, **kwargs):
        """

        :param aid:
        :param uid:
        :return:
        """
        uid = (int)(self.get_argument("uid"))
        aid = (int)(self.get_argument("aid"))
        try:
            ok, msg = SVC_Article.upcountArticleOnly(aid, uid)
        except Exception as e:
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            raise e

        if ok:
            self.write(dict(
                errcode=RET.RET_OK,
                errmsg=""
            ))
        else:
            self.write(dict(
                errcode = RET.RET_SERVERERR,
                errmsg = msg
            ))


def main():
    pass


if __name__ == '__main__':
    main()