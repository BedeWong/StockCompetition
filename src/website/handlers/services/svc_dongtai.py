#coding=utf-8

from handlers.models.basemodel import dbsession
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound

from handlers.models.tb_user_dongtai import UserDongtai, Dongtaitype

from handlers.services.svc_user_follower import SVC_UserFollower

class SVC_Dongtai(object):
    """
    動態類， 與數據庫交互
    """

    @staticmethod
    def add_dongtai(uid, type, fuid=0, extmsg="", aid=None):
        """
        添加一條動態
        :param uid:
        :param fuid:
        :param type:
        :param extmsg:
        :param aid:
        :return:
        """

        dongtai = UserDongtai()
        dongtai.u_id = uid
        dongtai.u_refuid = fuid
        dongtai.d_type = type
        dongtai.d_extmsg = extmsg
        dongtai.d_refaid = aid
        try:
            dbsession.add(dongtai)
            dbsession.commit()
        except Exception as e:
            dbsession.rollback()
            raise e

    @staticmethod
    def add_dongtai_follower(uid, fuid):
        """
        關注一個人， uid 關注fuid
        :param uid:
        :param fuid:
        :return:
        """

        SVC_Dongtai.add_dongtai(uid=uid, fuid=fuid, type=Dongtaitype.follower)


    @staticmethod
    def add_dongtai_reply(uid, fuid, content):
        """
        回復動態，
        :param uid:
        :param fuid:
        :param content:  内容摘要
        :return:
        """

        SVC_Dongtai.add_dongtai(uid=uid, fuid=fuid, type=Dongtaitype.reply, extmsg=content)


    @staticmethod
    def add_dongtai_upcont_topic(uid, fuid, aid, abscontent):
        """
        給話題點贊：
        :param uid:
        :param aid:
        :param abscontent:  文章標題摘要
        :return:
        """

        SVC_Dongtai.add_dongtai(uid, Dongtaitype.upcount_topic, fuid=fuid, aid=aid, extmsg=abscontent)


    @staticmethod
    def add_dongtai_upcont_reply(uid, fuid, aid, abscontent):
        """
        給話題點贊：
        :param uid:
        :param aid:
        :param abscontent:  文章標題摘要
        :return:
        """

        SVC_Dongtai.add_dongtai(uid, Dongtaitype.upcount_reply, fuid=fuid, aid=aid, extmsg=abscontent)

    @staticmethod
    def add_dongtai_pub_topic(uid, aid, content):
        """
        發表話題
        :param uid:
        :param aid:
        :param content:
        :return:
        """
        SVC_Dongtai.add_dongtai(uid, Dongtaitype.pub_topic, aid=aid, extmsg=content)

    @staticmethod
    def add_dongtai_pub_reply(uid, aid, content):
        """
        發表回復
        :param uid:
        :param aid:
        :param content:
        :return:
        """
        SVC_Dongtai.add_dongtai(uid, Dongtaitype.pub_topic, aid=aid, extmsg=content)


    @staticmethod
    def add_dongtai_trade(uid, detail):
        """
        下單股買股票
        :param uid:
        :param detail:  給定一個json串， 數據返回給前端，需要符合前端界面展示的要求
        :return:
        """

        SVC_Dongtai.add_dongtai(uid, Dongtaitype.buy_sale_stock, extmsg=detail)

    @staticmethod
    def add_dongtai_invoke(uid, detail):
        """
        下單股買股票
        :param uid:
        :param detail:  給定一個json串， 數據會返回給前端，需要符合前端界面展示的要求
        :return:
        """

        SVC_Dongtai.add_dongtai(uid, Dongtaitype.invoke_stock, extmsg=detail)

    @staticmethod
    def add_dongtai_mark_article(uid, aid):
        """
        下單股買股票
        :param uid:
        :param aid:  收藏的話題id
        :return:
        """

        SVC_Dongtai.add_dongtai(uid, Dongtaitype.mark_article, aid=aid)


    @staticmethod
    def get_dongtai_by_uid(uid, page=0, count=40):
        """
        返回一個uid的相關動態數據
        :param uid:
        :param page:
        :param count:
        :return:
        """

        res = None
        try:
            res = dbsession.query(UserDongtai).filter_by(u_id = uid).limit(count).offset(page*count).all()
        except Exception as e:
            dbsession.rollback()
            raise e

        if not res:
            return []

        lst = []
        for it in res:
            lst.append(it.to_json())

        return lst


    @staticmethod
    def get_dongtai_by_user(uid, page=0, count=40):
        """
        獲取與一個用戶相關的動態：獲取自己的  加上  關注的用戶的 動態
        :param uid:
        :param page:
        :param count:
        :return: 一個列表
        """

        follow_list = SVC_UserFollower.get_user_followers(uid)
        if not follow_list:
            return []

        res = None
        try:
            query = dbsession.query(UserDongtai).filter(UserDongtai.u_id.in_(follow_list))
            if count:
                query = query.limit(count)

            if page:
                query = query.offset(page*count)

            res = query.all()

        except Exception as e:
            dbsession.rollback()
            raise e

        if not res:
            return []

        lst = []
        for it in res:
            lst.append(it.to_json())

        return lst


def main():
    pass


if __name__ == '__main__':
    main()