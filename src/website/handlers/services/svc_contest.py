#coding=utf-8
from handlers.models.basemodel import dbsession
from handlers.models.tb_contest import Contest
from handlers.models.tb_contest_detail import ContestDetail
from handlers.models.tb_user import User


from sqlalchemy import and_, or_
from sqlalchemy.orm.exc import NoResultFound

from datetime import datetime
import logging

class SVC_Contest(object):
    """
    比賽相關數據庫操作
    """
    @staticmethod
    def add_contest(uid, title, desc, stime, etime, money, logo):
        """
        創建一個比賽：
        :param uid:
        :param title:  比賽標題
        :param desc:  描述
        :param stime:  開始時間：不能是當天或以前
        :param etime: 結束時間，不能小於開始時間
        :param money:  初始資金
        :param logo:  logo 圖片地址
        :return:
        """

        contest  = Contest()
        contest.u_id = uid
        contest.c_title = title
        contest.c_explain = desc
        contest.c_start_date = stime
        contest.c_end_date = etime
        contest.c_logo_url = logo
        contest.c_default_capital = money * 10000

        try:
            dbsession.add(contest)
            dbsession.commit()
        except Exception as e:
            dbsession.rollback()
            raise e

        return contest


    @staticmethod
    def get_contest_list(page=0, count=20):
        """
        獲取比賽列表：默認獲取的是未結束（關閉）的
        :param page:
        :param count:
        :return:
        """

        ret = None
        try:
            # ret = dbsession.query(Contest).all()
            # ret = dbsession.query(Contest).limit(count).offset(page * count).all()
            ret = dbsession.query(Contest, User.u_name).filter(Contest.u_id == User.id).order_by(Contest.c_create_time).limit(count).offset(page*count).all()
        except Exception as e:
            dbsession.rollback()
            raise e

        lst = []
        if ret:
            for it in ret:
                tmp = it[0].to_json()
                tmp['createuser'] = it[1]
                lst.append(tmp)

        return lst

    @staticmethod
    def close_contest(id):
        """
        關閉比賽, 結束比薩不在這裏處理，在每天的收盤后會有定時任務處理！
        :param id:
        :return:
        """

        test = None
        try:
            test = dbsession.query(Contest).filter(and_(Contest.id==id, Contest.c_status!=3, Contest.c_status!=2)).one()

            if test:
                test.c_status = 3    # 關閉

                dbsession.merge(test)
                dbsession.commit()
        except Exception as e:
            dbsession.rollback()
            raise e

    @staticmethod
    def join_contest(uid, id):
        """
        用戶參加比賽：根據id獲取比賽的相關信息，例如初始資金，將數據填入tb_contest_detail中
        :param uid:
        :param id:
        :return:
        """
        test = None
        user_contest_detail = None
        try:
            test = dbsession.query(Contest).filter_by(id=id).one()
        except Exception as e:
            dbsession.rollback()
            raise e

        try:
            user_contest_detail = dbsession.query(ContestDetail).filter(and_(ContestDetail.u_id == uid, ContestDetail.c_id==test.id)).one()
        except NoResultFound as e:
            pass
        except Exception as e:
            dbsession.rollback()
            raise e

        # 已經存在數據，説明已經加入比賽
        if user_contest_detail:
            raise Exception("已經加入該比賽！")

        user_contest_detail = ContestDetail()
        user_contest_detail.c_join_time = datetime.now()
        user_contest_detail.c_money = test.c_default_capital    # 初始資金
        user_contest_detail.c_id = test.id
        user_contest_detail.u_id = uid

        try:
            dbsession.add(user_contest_detail)
            dbsession.commit()
        except Exception as e:
            dbsession.rollback()
            raise e

    @staticmethod
    def quite_contest(uid, id):
        """
        用戶退出比賽
        :param uid:
        :param id:
        :return:
        """

        contest_detail = None
        try:
            contest_detail = dbsession.query(ContestDetail).filter(and_(ContestDetail.c_id==id, ContestDetail.u_id==uid)).one()
        except NoResultFound as e:
            return

        except Exception as e:
            dbsession.rollback()
            raise e

        contest_detail.c_status = 1

        try:
            dbsession.merge(contest_detail)
            dbsession.commit()
        except Exception as e:
            dbsession.rollback()
            raise e

    @staticmethod
    def get_user_contest_list(uid, all=False):
        """
        獲取用戶參加的比賽
        :param uid:
        :param all: 是否是已完成的  False:未結束的，  True 全部的
        :return:
        """

        res = None
        try:
            query = dbsession.query(Contest, ContestDetail, User.u_name)\
                .join(ContestDetail, Contest.id==ContestDetail.c_id)\
                .filter(ContestDetail.u_id==uid)\
                .join(User, User.id==Contest.u_id)
            # query = dbsession.query(ContestDetail, Contest, User.u_name).join(User, User.id==ContestDetail.u_id).filter(Contest.id==ContestDetail.c_id).filter(ContestDetail.u_id==uid)
            if not all:
                query = query.filter(or_(Contest.c_status==1, Contest.c_status==0))
            res = query.order_by(Contest.c_create_time).all()

            # print(query)
        except Exception as e:
            dbsession.rollback()
            raise e

        if not res:
            return []

        lst = []
        for it in res:
            contest_dct = it[0].to_json()
            contest_detail_dct = it[1].to_json()
            dct = contest_dct
            dct.update(contest_detail_dct)
            dct['createuser'] = it[2]
            lst.append(dct)

        return lst


    @staticmethod
    def get_contest_detail_rank_users(id, page=0, count=20):
        """
        獲取單個比賽的排名數據：
        :param id:  比賽id
        :return:
        """

        res = None
        try:
            res = dbsession.query(ContestDetail.c_win_rate, ContestDetail.u_id, User.u_name).filter(and_(ContestDetail.c_id==id, ContestDetail.c_status!=1)).join(User, User.id==ContestDetail.u_id).order_by(ContestDetail.c_win_rate.desc()).limit(count).offset(page*count).all()
        except Exception as e:
            dbsession.rollback()
            raise e

        lst = []
        if res:
            idx = 1
            for it in res:
                t = {}

                t['rate'] = it[0]           # 盈利率
                t['id'] = it[1]             # uid
                t['user'] = it[2]           # 用戶名
                t['rank'] = idx             # 排名
                lst.append(t)

                idx += 1
        return lst

    @staticmethod
    def check_user_in_contest(uid, id):
        """
        判斷用戶是否在比賽裏面
        :param uid:
        :param id:
        :return:   0 可加入， 1已加入， 2：已退出
        """

        contest_detail = None
        try:
            contest_detail = dbsession.query(ContestDetail).filter_by(c_id=id).filter_by(u_id=uid).one()
        except NoResultFound as e:
            return False
        except Exception as e:
            raise e

        if not contest_detail:
            return 0

        if contest_detail.c_status == 0:            # 已加入
            return 1
        elif contest_detail.c_status == 1:            # 已退出
            return 2


    @staticmethod
    def get_contest_user_info(uid, cid):
        """
        獲取用戶在某一場次比賽中的表現：
        :param uid:
        :param cid:
        :return:  json 串
        """

        info = None
        try:
            info = dbsession.query(ContestDetail, User.u_name, User.u_headurl).filter(and_(ContestDetail.u_id==uid, ContestDetail.c_id==cid)).join(User, User.id==ContestDetail.u_id).one()
        except NoResultFound as e:
            return []
        except Exception as e:
            dbsession.rollback()
            raise e

        logging.debug(info)
        if info:
            tmp = info[0].to_json()
            tmp['uname'] = info[1]
            tmp['uheadurl'] = info[2]
            return tmp
        return []


########################3 test
##
import traceback
def test_add_contest():
    try:
        ret = SVC_Contest.add_contest("27052237", "laji", "説明個毛綫", "2018-8-17", "2018-8-22", 50, "test.png")
    except Exception as e:
        traceback.print_exc()

    print(ret)

def test_get_contest_list():
    try:
        res = SVC_Contest.get_contest_list()
    except Exception as e:
        traceback.print_exc()

    print(res)

def test_join():
    try:
        SVC_Contest.join_contest("27152253", 5)
        SVC_Contest.join_contest("27152253", 3)
        SVC_Contest.join_contest("27052241", 5)
        SVC_Contest.join_contest("27052241", 3)
        SVC_Contest.join_contest("27052243", 5)
        SVC_Contest.join_contest("27052243", 3)
        SVC_Contest.join_contest("27052246", 5)
        SVC_Contest.join_contest("27052246", 3)
        SVC_Contest.join_contest("27152248", 5)
        SVC_Contest.join_contest("27152248", 3)
        SVC_Contest.join_contest("27152250", 5)
        SVC_Contest.join_contest("27152250", 3)
    except Exception as e:
        traceback.print_exc()

def test_get_user_contest_list():
    res = SVC_Contest.get_user_contest_list(27052237, all=True)

    for item in res:
        print(item)


def test_get_contest_detail_users():
    ret = SVC_Contest.get_contest_detail_rank_users(3)
    print(ret)
    ret = SVC_Contest.get_contest_detail_rank_users(2)
    print(ret)
    ret = SVC_Contest.get_contest_detail_rank_users(16)
    print(ret)
    ret = SVC_Contest.get_contest_detail_rank_users(17)
    print(ret)


def test_checkin():
    print ( SVC_Contest.check_user_in_contest(27052237, 3) )
    print(SVC_Contest.check_user_in_contest(27052237, 6))

    print(SVC_Contest.check_user_in_contest(27052237, 9))


def main():
    # test_add_contest()
    # test_get_contest_list()

    # test_join()
    test_get_user_contest_list()

    # test_get_contest_detail_users()

    # test_checkin()



if __name__ == '__main__':
    main()