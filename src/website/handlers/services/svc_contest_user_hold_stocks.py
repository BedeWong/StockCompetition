#coding=utf-8

from handlers.models.basemodel import dbsession

# exceptions
from sqlalchemy.orm.exc import NoResultFound

import logging

class SVC_UserStocks(object):
    """
    用戶持倉股票數據服務
    """

    # @staticmethod
    # def add_stock(uid, cid, stock_code, stock_name, stock_count, stock_price):
    #     """
    #     no return val
    #     raise 參數錯誤異常
    #     :param uid:
    #     :param:cid:比賽id
    #     :param stock_code:
    #     :param stock_name:
    #     :param stock_count:
    #     :param stock_price:  成本價
    #     :return:
    #     """
    #
    #     if not all([uid, stock_code, stock_name, stock_count, stock_price]):
    #         logging.error("參數錯誤：", uid, stock_code, stock_name, stock_count, stock_price)
    #         raise Exception("參數錯誤!")
    #
    #     ### 查詢是否已經買過該股票，是：添加持股數，否添加紀錄
    #     stock = None
    #     try:
    #         stock = dbsession.query(UserStock).filter_by(u_id=uid).filter_by(s_stock_code=stock_code).one()
    #     except NoResultFound as e:
    #         dbsession.rollback()
    #         logging.error(e)
    #
    #     # 沒記錄，沒買過
    #     if stock is None:
    #         stock = UserStock()
    #         stock.u_id = uid
    #         stock.c_id = cid
    #         stock.s_stock_price = stock_price
    #         stock.s_stock_code = stock_code
    #         stock.s_stock_name = stock_name
    #         stock.s_stock_count = stock_count
    #
    #         try:
    #             dbsession.add(stock)
    #             dbsession.commit()
    #         except Exception as e:
    #             dbsession.rollback()
    #             logging.error(e)
    #             raise e
    #
    #     else:
    #         price = ((float)(stock.s_stock_price) * stock.s_stock_count + stock_price*stock_count) / (stock.s_stock_count+stock_count)
    #         stock.s_stock_count += stock_count
    #         stock.s_stock_price = price
    #
    #         try:
    #             dbsession.merge(stock)
    #             dbsession.commit()
    #         except Exception as e:
    #             dbsession.rollback()
    #             logging.error(e)
    #             raise e
    #
    # @staticmethod
    # def sale_stock(uid, cid, stock_code, stock_name, stock_count):
    #     """
    #     賣出
    #     :param uid:
    #     :param stock_code:
    #     :param stock_name:
    #     :param stock_count:
    #     :return: if success return True,"" ortherwise return False, "errmsg"  or raise the exceptions
    #     """
    #     if not all([uid, stock_code, stock_name, stock_count, cid]):
    #         logging.error("參數錯誤：", uid, stock_code, stock_name, stock_count)
    #         raise Exception("參數錯誤!")
    #
    #     if not all( [isinstance(uid, str),  isinstance(stock_code, str),
    #                 isinstance(stock_name, str), isinstance(stock_count, int), isinstance(cid, int)]):
    #         logging.error("參數錯誤：", uid, stock_code, stock_name, stock_count)
    #         raise Exception("參數錯誤!")
    #
    #     # 查詢是否已經購買此股
    #     stock = None
    #     try:
    #         stock = dbsession.query(UserStock).filter_by(u_id=uid).filter_by(c_id=cid).filter_by(s_stock_code=stock_code).one()
    #     except NoResultFound as e:
    #         dbsession.rollback()
    #         logging.error(e)
    #
    #     if stock == None:
    #         logging.info("用戶沒有持有持有該股票：", uid, stock_code)
    #         return False, "沒有持有持有該股票"
    #
    #     ### 剛好清倉
    #     if stock.s_stock_count == stock_count:
    #         try:
    #             dbsession.delete(stock)
    #             dbsession.commit()
    #         except Exception as e:
    #             logging.error(e)
    #             dbsession.rollback()
    #             raise e
    #     ## 數據有錯誤
    #     elif stock.s_stock_count < stock_count:
    #         logging.info("用戶未持有這麽多股份：", uid, stock_code, stock_count)
    #         return False, "未持有這麽多股份"
    #
    #     #正常買出
    #     else:
    #         stock.s_stock_count -= stock_count
    #         try:
    #             dbsession.merge(stock)
    #             dbsession.commit()
    #         except Exception as e:
    #             logging.error(e)
    #             dbsession.rollback()
    #             raise e
    #
    #     return True, ""


    @staticmethod
    def get_stock_list(uid, cid, page=1, lmt=100):
        """
        列出用戶的持股信息，默認100條
        return: a list,
        :param uid:
        :param cid:
        :param page:
        :param lmt:
        """
        if not all((uid, cid)):
            logging.error("uid err", uid)
            raise Exception("parameter err")

        sql = "select * from tb_user_contest_positions where user_id = %s and stock_count > 0 and contest_id=%d" \
              " order by updated_at desc" \
              " limit %d, %d" % (uid, cid, (page-1)*lmt, lmt)
        result = []
        try:
            query_res = dbsession.execute(sql)
            dbsession.commit()
            query_res = query_res.fetchall()
        except Exception as e:
            dbsession.rollback()
            logging.error(e)
            raise

        # table column
        headers = ("id", "created_at", "updated_at", "deleted_at",
                   "uid", "name", "code", "count", "price",
                   "freeze", "cid")
        for item in query_res:
            dct = dict(zip(headers, item))

            tm = dct['created_at']
            dct['created_at'] = tm.strftime("%Y-%m-%d %H:%M:%S") if tm else None
            tm = dct['updated_at']
            dct['updated_at'] = tm.strftime("%Y-%m-%d %H:%M:%S") if tm else None
            tm = dct['deleted_at']
            dct['deleted_at'] = tm.strftime("%Y-%m-%d %H:%M:%S") if tm else None

            dct['price'] = float(dct['price'])
            dct['freeze'] = float(dct['freeze'])

            result.append(dct)

        return result

#####################################################################3
#####   test

import  traceback
def test_add():
    try:
        SVC_UserStocks.add_stock("27052237", 3, "sh600225", "天津松江", 10, 15.89)
        SVC_UserStocks.add_stock("27052237", 3, "sh600225", "天津松江", 17, 17.89)
        SVC_UserStocks.add_stock("27052237", 3, "sz300154", "瑞凌股份", 77, 2.89)
        SVC_UserStocks.add_stock("27052237", 3, "sz300154", "瑞凌股份", 10, 4.70)
        SVC_UserStocks.add_stock("27052237", 3, "sz300306", "远方信息", 12, 5.33)
        SVC_UserStocks.add_stock("27052237", 3, "sz300154", "瑞凌股份", 1340, 115.289)
    except Exception as e:
        traceback.print_exc()
        print(e)

def test_del():
    try:
        ret = SVC_UserStocks.sale_stock("27052237", 3, "sh600225", "天津松江", 5)
        print("27052237", "sh600225", "天津松江", 5, "---", ret)

        ret = SVC_UserStocks.sale_stock("27052237", 3, "sh600225", "天津松江", 9)
        print("27052237", "sh600225", "天津松江", 9, "---", ret)

        ret = SVC_UserStocks.sale_stock("27052237", 3, "sz300306", "远方信息", 9)
        print("27052237", "sz300306", "远方信息", 5, "---", ret)

        ret = SVC_UserStocks.sale_stock("27052237", 3, "sz300306", "远方信息", 9)
        print("27052237", "sz300306", "远方信息", 5, "---", ret)

        ret = SVC_UserStocks.sale_stock("27052237", 3, "sz300154", "瑞凌股份", 9)
        print("27052237", "sz300154", "瑞凌股份", 9, "---", ret)

    except Exception as e:
        traceback.print_exc()
        print(e)

def test_get_lst():
    try:
        res = SVC_UserStocks.get_stock_list(27052237, 3)
    except Exception as e:
        traceback.print_exc()
        print(e)

    print(res)


def main():
    # test_add()
    test_get_lst()
    # test_del()


if __name__ == '__main__':
    main()