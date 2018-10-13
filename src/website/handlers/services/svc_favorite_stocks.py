#coding=utf-8

from handlers.models.basemodel import dbsession
from handlers.models.tb_user_favorite_stocks import UserFavoriteStocks

# exceptions
from sqlalchemy.orm.exc import NoResultFound

import logging

class SVC_FavoriteStocks(object):
    """
    用戶自選股列表，用戶的自選股操作
    """

    @staticmethod
    def add_stock(uid, stock_code, stock_name):
        if uid == None or uid == '':
            logging.info("uid is None..")
            return

        if len(stock_code) == 0 or len(stock_name) == 0:
            logging.info("stock_code, stock_name 不合法..")
            return

        try:
            stock = dbsession.query(UserFavoriteStocks).filter_by(u_id=uid).filter_by(s_stock_code=stock_code).one()
        except NoResultFound as e:
            stock = None

        if stock is not None:
            return "exist"

        stock = UserFavoriteStocks()
        stock.u_id = uid
        stock.s_stock_code = stock_code
        stock.s_stock_name = stock_name

        dbsession.add(stock)
        dbsession.commit()

    @staticmethod
    def del_stock(uid, stock_code):
        if uid is None or uid == '':
            logging.error("uid 不合法:", uid)
            raise Exception("Parameter error.")

        if stock_code is None or stock_code == '':
            logging.error("stock_code 不合法:", stock_code)
            raise Exception("Parameter error.")

        try:
            stock = dbsession.query(UserFavoriteStocks).filter_by(u_id=uid).filter_by(s_stock_code=stock_code).one()
        # 找不到數據會抛出NoResultFound異常，補貨，不做處理,正常執行下面流程
        except NoResultFound as e:
            stock = None

        if (stock is not None):
            dbsession.delete(stock)
            dbsession.commit()
        else:
            logging.error("stock:%s不存在" % (stock_code))

    @staticmethod
    def check_stock(uid, stock_code):
        """
        查找是否是自選股
        :param uid:   用戶id
        :param stock_code: 股票代碼：如 sh600036
        :return:
        """

        if not isinstance(uid, str) or not isinstance(stock_code, str):
            logging.error("函數參數錯誤！", uid, stock_code)
            raise TypeError("函數參數錯誤")

        retval = False

        try:
            stock = dbsession.query(UserFavoriteStocks).filter_by(u_id=uid, s_stock_code=stock_code).one()
        except NoResultFound:
            stock = None

        if stock:
            retval = True

        return retval

    @staticmethod
    def get_stocks(uid, lmt=100):
        if not isinstance(uid, str) or not isinstance(lmt, int):
            logging.error("參數類型錯誤:", uid, lmt)
            raise TypeError("參數類型錯誤")


        ret = dbsession.query(UserFavoriteStocks).filter_by(u_id=uid).limit(lmt).all()

        res = []
        for it in ret:
            res.append(it.to_json())

        # test
        sz = len(res)
        logging.debug("get_stocks: ret.length:", sz)
        return res


###########################  TEST...
#
#
# import unittest
#
# class TestFavoriteService(unittest.TestCase):
#
#     def setUp(self):
#         # Do something to initiate the test environment here.
#         pass
#
#     def tearDown(self):
#         # Do something to clear the test environment here.
#         pass
#
#     @classmethod
#     def tearDownClass(self):
#          print('TestFavoriteService  over.')
#
#     @classmethod
#     def setUpClass(self):
#         print('TestFavoriteService  begin.')


import traceback
def test_add():
    try:
        SVC_FavoriteStocks.add_stock("27052237", "sh600225", "天津松江")
        SVC_FavoriteStocks.add_stock("27052237", "sz300154", "瑞凌股份")
        SVC_FavoriteStocks.add_stock("27052237", "sz300306", "远方信息")
        SVC_FavoriteStocks.add_stock("27052237", "sz300154", "瑞凌股份")
        SVC_FavoriteStocks.add_stock("27052237", "sh600225", "")
    except Exception as e:
        print(e)
        traceback.print_exc()

def test_getlist():
    try:
        ret = SVC_FavoriteStocks.get_stocks("27052237")
        print(ret)
    except Exception as e:
        print(e)
        traceback.print_exc()

def test_check():
    try:
        ret = SVC_FavoriteStocks.check_stock("27052237", "sh600225")
        print("27052237 sh600225:", ret)

        ret = SVC_FavoriteStocks.check_stock("27052237", "sh600225")
        print("27052237 sh600225:", ret)

        ret = SVC_FavoriteStocks.check_stock("27052237", "sh600999")
        print("27052237 sh600225:", ret)
    except Exception as e:
        print(e)
        traceback.print_exc()

def test_del():
    try:
        SVC_FavoriteStocks.del_stock("27052237", "sz300154")
        SVC_FavoriteStocks.del_stock("27052237", "sz300154")
        SVC_FavoriteStocks.del_stock("27052237", "sh600225")
    except Exception as e:
        print(e)
        traceback.print_exc()

def main():

    test_add()
    # test_check()
    test_getlist()
    # test_del()


if __name__ == '__main__':
    main()