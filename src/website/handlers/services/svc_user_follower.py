#coding=utf-8

from sqlalchemy import and_, func
from sqlalchemy.orm.exc import NoResultFound

from handlers.models.basemodel import dbsession
from handlers.models.tb_user_followers import UserFollowers

class SVC_UserFollower(object):
    """
    用戶粉絲關係處理類
    """

    @staticmethod
    def add_recode(uid, fuid):
        """
        用戶關注一個用戶
        :param uid:  被關注人
        :param fuid:  關注人
        :return:
        """

        recode = UserFollowers()
        recode.u_id = uid,
        recode.u_follower_id = fuid
        try:
            dbsession.add(recode)
            dbsession.commit()
        except Exception as e:
            dbsession.rollback()
            raise e



    @staticmethod
    def del_recode(uid, fuid):
        """
        用戶取關
        :param uid:  被關注的用戶u
        :param fuid: 關注者
        :return:
        """

        recode = None
        try:
            dbsession.query(UserFollowers).filter(and_(UserFollowers.u_id==uid, UserFollowers.u_follower_id==fuid)).one()
        except NoResultFound as e:
            return

        if not recode:
            return

        try:
            dbsession.delete(recode)
            dbsession.commit()
        except Exception as  e:
            dbsession.rollback()
            raise e


    @staticmethod
    def get_user_followers_count(uid):
        """
        獲取用戶的粉絲計數
        :param uid:
        :return:
        """

        count = 0
        try:
            count = dbsession.query(func.count(1)).filter(UserFollowers.u_id == uid).scalar()
        except Exception as e:
            dbsession.rollback()
            raise  e

        if not count:
            return 0

        return count


    @staticmethod
    def get_user_followers(uid):
        """
        獲取用戶關注的人列表
        :param uid:
        :return:
        """

        lst = None
        try:
            lst = dbsession.query(UserFollowers.u_id).filter(UserFollowers.u_follower_id==uid).all()
        except Exception as e:
            dbsession.rollback()

        if not lst:
            return []

        return lst


    @staticmethod
    def check_user_folower_relation(uid, fuid):
        """
        檢測用戶是不是粉絲關係
        :param uid:    被關注的人
        :param fuid:   粉絲
        :return:  True or False
        """

        res = None
        try:
            res = dbsession.query(UserFollowers).filter(and_(UserFollowers.u_follower_id==fuid, UserFollowers.u_id==uid)).one()
        except NoResultFound as e:
            return False

        if res:
            return True

        return False


def main():
    pass


if __name__ == '__main__':
    main()