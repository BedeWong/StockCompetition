#coding=utf-8

from handlers.models.basemodel import dbsession

from handlers.services.svc_dongtai import SVC_Dongtai
import config

# exceptions
from sqlalchemy.orm.exc import NoResultFound

import logging
import  traceback
import json
import time
import hashlib
import requests

class SVC_TradeRecode(object):
    """
    对接rpc接口
    """
    @staticmethod
    def add_order(uid, type, price, amount, code, name, contest_id=0):
        """
        委托下单
        :param uid: 用戶id
        :param type: B/S  1買入  2 賣出
        :param price:  價格
        :param amount:  成交量
        :param code:    股票代碼
        :param name:  股票名字
        :param contest_id: 比赛场次，非0为比赛下单（代码耦合了）
        :return:  no val, if err throw exception
        """

        if type not in [1,2]:
            logging.error("type err", type)
            raise Exception("type err")

        # volume = amount * price
        # charge = round(volume * 0.00025, 2)    # 此值應該存放在配置中！！
        # if charge < 5 :
        #     charge = 5
        #
        # recode = TradeRecode()
        # recode.t_volume = volume
        # recode.t_stock_price = price
        # recode.t_stock_amount = amount
        # recode.t_charge = charge
        # recode.t_type = type
        # recode.s_name = name
        # recode.s_code = code
        # recode.u_id = uid
        #
        # recode.s_id = 0   ## exception  這個值不能為0
        #
        # try:
        #     user = None
        #     ### 取出用戶的數據，檢測是否餘額是否足夠
        #     try:
        #         user = dbsession.query(User).filter_by(id=uid).one()
        #     except Exception as e:   #  包括了NoResultFound異常， 用戶的數據都找不到了，還處理個毛綫
        #         logging.error(e)
        #         dbsession.rollback()
        #         raise e
        #
        #     #### 買入
        #     if type == 1:
        #         if user.u_money < volume + charge:
        #             logging.info("用戶的餘額不足.", uid)
        #             raise  Exception("餘額不足")
        #
        #         user.u_money = (float)(user.u_money) - volume     #  凍結用戶的資產
        #     user.u_money = (float)(user.u_money) - charge         #  賣出的手續費一樣在這裏扣除
        #
        #
        #     dbsession.merge(user)
        #     dbsession.add(recode)
        #     dbsession.commit()
        # except Exception as e:
        #     dbsession.rollback()
        #     logging.error(e)
        #     raise e
        #

        now = str(time.time())

        sign = ''.join(sorted(str(uid) + now + config.RPC_REQUEST_SALT))
        md5 = hashlib.md5()
        md5.update(sign.encode())
        sign = md5.hexdigest()
        request_body = {
            "method": "orderService.AddOrder",
            "params":[{
                "user_id": uid,
                "sign": sign,
                "stock_code": code,
                "stock_name": name,
                "stock_count": amount,
                "stock_price": price,
                "trade_type": type,
                "req_time": now,
                "contest_id": contest_id,
            }]
        }

        try:
            resp = requests.post(config.RPC_SERVICE_URL,
                                 json=request_body,
                                 headers={'Content-Type': 'application/json'})
        except Exception as e:
            raise

        if not resp.ok:
            raise Exception("请求失败, 请稍后再试!")

        content = resp.content.decode()
        content = json.loads(content)['result']
        if content['ret_code'] != 0 :
            raise Exception(content['err_msg'])

        # 添加用户动态.
        data = {
            'uid': 'uid',
            'code': code,
            'name':name,
            'contest_id':contest_id,
            'type': '买入' if type == 1 else '卖出',
        }
        try:
            SVC_Dongtai.add_dongtai_trade(uid, json.dumps(data))
        except Exception as e:
            logging.error(e)
            raise

    @staticmethod
    def get_recode_list(uid, type=0, page=1, count=40, cid=0):
        """
        獲取用戶的交易記錄: 已成交
        :param uid:
        :param type:  0：所有的   1買入  2 賣出
        :param page:    頁
        :param count:   每頁加載數據量
        :param cid： 比赛id
        :return: a list container all objects
        """
        if not all([isinstance(type, int), isinstance(page, int),isinstance(count, int)]):
            logging.error("parameter type err:")
            raise Exception("parameter type err:")

        sql = "select * from tb_trade_details "
        where = " where "
        limit = " limit %d, %d " % ((page-1)*count, count)

        # where 条件
        where_cond = ["user_id=%s" % uid, "contest_id=%d" % cid]
        try:
            if type != 0:
                where_cond.append("trade_type=%d" % type )

            # 组装where条件
            where += " and ".join(where_cond)
            sql += where + " order by updated_at desc " + limit

            # 执行sql
            logging.debug(sql)
            result = dbsession.execute(sql).fetchall()
        except Exception as e:
            logging.error(e)
            raise

        res = []
        if result is None:
            return res

        # 组装数据
        colums = ("id", "created_at", "updated_at", "deleted_at", "order_id", "uid",
                  "name", "code", "price", "amount", "type", "charge", "cid")
        for item in result:
            dct = dict(zip(colums, item))
            dct['volume'] = round(
                (float)(dct['price'])*(float)(dct['amount']),
                2)
            res.append(dct)

        return res

    @staticmethod
    def revoke_order(uid, order_id, contest_id=0):
        """
        撤銷一個訂單：
        :param uid: 用戶id
        :param order_id:   訂單id號
        :param contest_id:   比赛id， 0表示非比赛（代码耦合了）
        :return:
        """

        if not isinstance(order_id, int):
            logging.error("id not a int object %s", id)
            raise Exception("參數錯誤")

        # recode = None
        # try:
        #     recode = dbsession.query(TradeRecode).filter_by(id=id).filter_by(u_id=uid).one()
        # except NoResultFound as e:
        #     logging.warning(e)
        #     dbsession.rollback()
        #     raise e
        #
        # except Exception as e:
        #     logging.error(e)
        #     dbsession.rollback()
        #     raise e
        #
        # ## 判斷用記錄的狀態是否對
        # if recode.t_status != 0:
        #     logging.error("記錄的狀態不對, 不能撤銷該訂單: %s" %(recode.to_json()) )
        #     raise Exception("記錄的狀態不對, 不能撤銷該訂單")
        #
        # user = None
        # ### 取出用戶的數據，檢測是否餘額是否足夠
        # try:
        #     user = dbsession.query(User).filter_by(id=uid).one()
        # except NoResultFound as e:   #  包括了NoResultFound異常， 用戶的數據都找不到了，還處理個毛綫
        #     logging.error(e)
        #     raise e
        # except Exception as e:
        #     dbsession.rollback()
        #     logging.error(e)
        #     raise e
        #
        # if recode.t_type == 1:    # 買入
        #     user.u_money = (float)(user.u_money) + (float)(recode.t_volume) + (float)(recode.t_charge)   # 用戶的錢返還回去
        # elif recode.t_type == 2:  # 賣出  退還凍結的手續費
        #     user.u_money = (float)(user.u_money) + (float)(recode.t_charge)
        #
        # recode.t_status = 2                             # 記錄狀態設置為撤單
        # try:
        #     dbsession.merge(recode)
        #     dbsession.merge(user)
        #     dbsession.commit()
        # except Exception as e:
        #     dbsession.rollback()
        #     logging.error(e)
        #     raise e

        # 检测订单数据
        sql = 'select * from tb_orders where user_id=%d and id=%d ' % (uid, order_id)
        try:
            result = dbsession.execute(sql).fetchall()
            if not result:
                raise Exception("订单数据不存在. order_id: %d, user_id: %d" %(order_id, uid))
        except Exception as e:
            logging.error("数据库错误：%s", e)
            raise

        # 拼接数据
        colums = ("id", "created_at", "updated_at", "deleted_at",
                  "uid", "name", "code", "price", "count", "transfer_fee",
                  "brokerage", "freeze_amount", "trade_type", "type",
                  "status", "contest_id")
        record = dict(zip(colums, result[0]))
        # 检查订单状态
        # enum:
        #   ORDER_STATUS_TBD = iota
        # 	ORDER_STATUS_FINISH
        # 	ORDER_STATUS_REVOKE
        if record['status'] != 0:
            raise Exception("撤销订单失败,订单状态不对.")

        # 构造请求，发送到交易服务器
        now = str(time.time())

        sign = ''.join(sorted(str(uid) + now + config.RPC_REQUEST_SALT))
        md5 = hashlib.md5()
        md5.update(sign.encode())
        sign = md5.hexdigest()
        request_body = {
            "method": "orderService.RevokeOrder",
            "params": [{
                "user_id": uid,
                "sign": sign,
                "order_id": order_id,
                "req_time": now,
                "contest_id": contest_id,
            }]
        }

        try:
            resp = requests.post(config.RPC_SERVICE_URL,
                                 json=request_body,
                                 headers={'Content-Type': 'application/json'})
        except Exception as e:
            raise

        if not resp.ok:
            raise Exception("请求失败, 请稍后再试!")

        content = resp.content.decode()
        content = json.loads(content)['result']
        if content['ret_code'] != 0:
            raise Exception(content['err_msg'])

        # 添加用户动态.
        data = {
            'uid': record['uid'],
            'order_id': record['id'],
            'code': record['code'],
            'name': record['name'],
            'contest_id': record['contest_id'],
            'type': record['type'],
        }
        try:
            SVC_Dongtai.add_dongtai_revoke(uid, json.dumps(data))
        except Exception as e:
            logging.error(e)
            raise e

    @staticmethod
    def list_orders(uid, cid, type=None, page=1, count=40):
        """
        获取订单列表.
        :param uid: 用户id
        :param cid: 比赛id （0为非比赛委托单）
        :param page:
        :param count:
        :param type:  交易类型
                TRADE_TYPE_NONE = iota
                TRADE_TYPE_BUY  # 买入
                TRADE_TYPE_SALE  # 卖出
        :return:
        """
        uid = (int)(uid)
        cid = (int)(cid)
        page = (int)(page)
        count = (int)(count)

        sql = 'select * from tb_orders where '
        where_cond = ['user_id=%d' % uid, 'contest_id=%d' % cid,]
        order_by = ' order by updated_at desc '
        limit_sql = ' limit %d, %d ' % ((page-1)*count, count)

        if type is not None:
            # 交易类型过滤
            where_cond.append('trade_type=%d' % type)

        # 执行sql
        sql = sql + ' and '.join(where_cond) + \
                order_by + limit_sql
        logging.debug('sql: %s' % sql)

        raws = dbsession.execute(sql).fetchall()
        if not raws:
            return []

        # table colume
        colums = ('id', 'created_at', 'updated_at', 'deleted_at', 'uid',
                  'name', 'code', 'price', 'count', 'transfer_fee',
                  'brokerage', 'total_value', 'trade_type', 'type',
                  'status', 'cid')
        result = []
        for item in raws:
            dct = dict(zip(item, colums))
            result.append(dct)

        return result


#####################################################################3
#####   test

def test_add():
    try:
        # SVC_TradeRecode.add_order(27052237, 1, 2.88, 1103, "sz002729", "好利来")
        # SVC_TradeRecode.add_order(27052237, 1, 9.88, 103, "sz002729", "好利来")
        # SVC_TradeRecode.add_order(27052237, 2, 1.44, 1203, "sz002679", "福建金森")
        # SVC_TradeRecode.add_order(27052237, 1, 3.12, 123, "sz002679", "福建金森")
        SVC_TradeRecode.add_order(27052237, 2, 13.58, 103, "sh600050", "中国联通")
        SVC_TradeRecode.add_order(27052237, 1, 5.18, 103, "sh600037", "歌华有线")
    except Exception as e:
        traceback.print_exc()

def test_get_list():
    try:
        lst = SVC_TradeRecode.get_recode_list("27052243", 0)
        print(lst)

        lst = SVC_TradeRecode.get_recode_list("27052243", 0, 2)
        print(lst)

        lst = SVC_TradeRecode.get_recode_list("27052243", 1)
        print(lst)

        lst = SVC_TradeRecode.get_recode_list("27052243", 2)
        print(lst)
    except Exception as e:
        traceback.print_exc()

def test_invoke_recode():
    try:
        SVC_TradeRecode.revoke_order(27052242, 24)
        SVC_TradeRecode.revoke_order(27052243, 21)
    except Exception as e:
        traceback.print_exc()


def test_list_orders():
    try:
        print(SVC_TradeRecode.list_orders(27052242, 0))
        print(SVC_TradeRecode.list_orders(27052242, 2))
        print(SVC_TradeRecode.list_orders(27052242, 0, 1)) # 买入
        print(SVC_TradeRecode.list_orders(27052237, 0, 2))
    except Exception as e:
        traceback.print_exc()

def main():
    # test_add()
    # test_get_list()
    # test_invoke_recode()
    test_list_orders()


if __name__ == '__main__':
    main()