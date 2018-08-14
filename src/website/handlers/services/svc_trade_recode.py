#coding=utf-8

from handlers.models.basemodel import dbsession
from handlers.models.tb_user_trade_recode import TradeRecode
from handlers.models.tb_user import User

# exceptions
from sqlalchemy.orm.exc import NoResultFound

import logging
import  traceback

class SVC_TradeRecode(object):
    """
    提供trade recode表的操作：
    """

    @staticmethod
    def add_recode(uid, type, price, amount, code, name):
        """
        添加一條記錄：
            買入： 凍結用戶餘額，餘額不足不能繼續處理
            賣出：扣除交易手續費，用戶成交的額度在交易系統中給用戶處理
        :param uid: 用戶id
        :param type: B/S  1買入  2 賣出
        :param price:  價格
        :param amount:  成交量
        :param code:    股票代碼
        :param name:  股票名字
        :return:  no val, if err throw exception
        """

        if type not in [1,2]:
            logging.error("type err", type)
            raise Exception("type err")

        volume = amount * price
        charge = round(volume * 0.00025, 2)    # 此值應該存放在配置中！！
        if charge < 5 :
            charge = 5

        recode = TradeRecode()
        recode.t_volume = volume
        recode.t_stock_price = price
        recode.t_stock_amount = amount
        recode.t_charge = charge
        recode.t_type = type
        recode.s_name = name
        recode.s_code = code
        recode.u_id = uid

        recode.s_id = 0   ## exception  這個值不能為0

        try:
            user = None
            ### 取出用戶的數據，檢測是否餘額是否足夠
            try:
                user = dbsession.query(User).filter_by(id=uid).one()
            except Exception as e:   #  包括了NoResultFound異常， 用戶的數據都找不到了，還處理個毛綫
                logging.error(e)
                dbsession.rollback()
                raise e

            #### 買入
            if type == 1:
                if user.u_money < volume + charge:
                    logging.info("用戶的餘額不足.", uid)
                    raise  Exception("餘額不足")

                user.u_money = (float)(user.u_money) - volume     #  凍結用戶的資產
            user.u_money = (float)(user.u_money) - charge         #  賣出的手續費一樣在這裏扣除


            dbsession.merge(user)
            dbsession.add(recode)
            dbsession.commit()
        except Exception as e:
            dbsession.rollback()
            logging.error(e)
            raise e


    @staticmethod
    def get_recode_list(uid, type=0, page=1, limit=40, ext=None):
        """
        獲取用戶的交易記錄（不管是否已成交）
        :param uid:
        :param type:  0：所有的   1買入  2 賣出
        :param page:    頁
        :param limit:   每頁加載數據量
        :param ext： 選項  finished 只加載已完成   unfinished 只加載未完成 all 加載所有
        :return: a list container all objects
        """

        lst = None
        if not all([isinstance(type, int), isinstance(page, int),isinstance(limit, int)]):
            logging.error("parameter type err:")
            raise Exception("parameter type err:")

        try:
            query = dbsession.query(TradeRecode).filter_by(u_id=uid)

            if type != 0:
                query = query.filter_by(t_type=type)

            ##### finished 已完成的
            ##### unfinished 未完成的
            ##### all 所有的
            if ext == 'finished':
                query = query.filter_by(t_status=1)
            elif ext == 'unfinished':
                query = query.filter_by(t_status=0)
            elif ext == 'all':
                pass
            else:
                logging.warning("ext parameter err. %s", ext)

            lst = query.limit(limit).offset((page-1)*limit).all()
        except Exception as e:
            dbsession.rollback()
            logging.error(e)
            raise e

        res = []
        if lst is None:
            return res

        for it in lst:
            res.append(it.to_json())

        return res

    @staticmethod
    def revoke_order(uid, id):
        """
        撤銷一個訂單：
        :param uid: 用戶id
        :param id:   訂單id號
        :return:
        """

        if not isinstance(id, int):
            logging.error("id not a int object %s", id)
            raise Exception("參數錯誤")

        recode = None
        try:
            recode = dbsession.query(TradeRecode).filter_by(id=id).filter_by(u_id=uid).one()
        except NoResultFound as e:
            logging.warning(e)
            dbsession.rollback()
            raise e

        except Exception as e:
            logging.error(e)
            dbsession.rollback()
            raise e

        ## 判斷用記錄的狀態是否對
        if recode.t_status != 0:
            logging.error("記錄的狀態不對, 不能撤銷該訂單: %s" %(recode.to_json()) )
            raise Exception("記錄的狀態不對, 不能撤銷該訂單")

        user = None
        ### 取出用戶的數據，檢測是否餘額是否足夠
        try:
            user = dbsession.query(User).filter_by(id=uid).one()
        except NoResultFound as e:   #  包括了NoResultFound異常， 用戶的數據都找不到了，還處理個毛綫
            logging.error(e)
            raise e
        except Exception as e:
            dbsession.rollback()
            logging.error(e)
            raise e

        if recode.t_type == 1:    # 買入
            user.u_money = (float)(user.u_money) + (float)(recode.t_volume) + (float)(recode.t_charge)   # 用戶的錢返還回去
        elif recode.t_type == 2:  # 賣出  退還凍結的手續費
            user.u_money = (float)(user.u_money) + (float)(recode.t_charge)

        recode.t_status = 2                             # 記錄狀態設置為撤單
        try:
            dbsession.merge(recode)
            dbsession.merge(user)
            dbsession.commit()
        except Exception as e:
            dbsession.rollback()
            logging.error(e)
            raise e


#####################################################################3
#####   test

def test_add():
    try:
        SVC_TradeRecode.add_recode("27052237", 1, 2.88, 1103, "sz002729", "好利来")
        SVC_TradeRecode.add_recode("27052237", 1, 9.88, 103, "sz002729", "好利来")
        SVC_TradeRecode.add_recode("27052237", 2, 1.44, 1203, "sz002679", "福建金森")
        SVC_TradeRecode.add_recode("27052237", 1, 3.12, 123, "sz002679", "福建金森")
        SVC_TradeRecode.add_recode("27052237", 2, 13.58, 103, "sh600050", "中国联通")
        SVC_TradeRecode.add_recode("27052237", 1, 5.18, 103, "sh600037", "歌华有线")
    except Exception as e:
        traceback.print_exc()

def test_get_list():
    try:
        lst = SVC_TradeRecode.get_recode_list("27052237", 0)
        print(lst)

        lst = SVC_TradeRecode.get_recode_list("27052237", 0, 2)
        print(lst)

        lst = SVC_TradeRecode.get_recode_list("27052237", 1)
        print(lst)

        lst = SVC_TradeRecode.get_recode_list("27052237", 2)
        print(lst)
    except Exception as e:
        traceback.print_exc()

def test_invoke_recode():
    try:
        SVC_TradeRecode.revoke_order("27052237", 35)
        SVC_TradeRecode.revoke_order("27052237", 37)
        SVC_TradeRecode.revoke_order("27052237", 37)
    except Exception as e:
        traceback.print_exc()


def main():
    # test_add()
    test_get_list()
    # test_invoke_recode()


if __name__ == '__main__':
    main()