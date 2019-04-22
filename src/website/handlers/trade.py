#coding=utf-8

import logging
from utils.commons import required_login

from utils.response_code import RET, RETMSG_MAP
from handlers.basehandler import BaseHandler

from handlers.services.svc_trade_recode import SVC_TradeRecode


class BuyStockHander(BaseHandler):
    """
    下訂單
    """
    @required_login
    def post(self, *args, **kwargs):
        """

        :return:
        """
        u_id = int(self.get_argument("uid"))
        stock_code = self.get_argument("code")
        stock_name = self.get_argument("name")
        stock_price = (float)(self.get_argument("price"))
        stock_amount = (int)(self.get_argument("amount"))

        try:
            SVC_TradeRecode.add_order(u_id, 1, stock_price, stock_amount, stock_code, stock_name)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode = RET.RET_SERVERERR,
                errmsg = RETMSG_MAP[RET.RET_SERVERERR]
            ))
            return

        self.write(dict(
            errcode = RET.RET_OK,
            errmsg = ""
        ))


class SaleStockHandler(BaseHandler):
    """
    委托卖单
    """
    @required_login
    def post(self, *args, **kwargs):
        u_id = int(self.get_argument("uid"))
        stock_code = self.get_argument("code")
        stock_name = self.get_argument("name")
        stock_price = (float)(self.get_argument("price"))
        stock_amount = (int)(self.get_argument("amount"))

        try:
            SVC_TradeRecode.add_order(u_id, 2, stock_price, stock_amount, stock_code, stock_name)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            return

        self.write(dict(
            errcode=RET.RET_OK,
            errmsg=""
        ))


class GetTradeHistoryHandler(BaseHandler):
    """
    獲取交易歷史記錄
    """
    @required_login
    def get(self, *args, **kwargs):
        """

        :return:
        """
        u_id = (int)(self.get_argument("uid"))
        c_id = (int)(self.get_argument('cid'))
        type = (int)(self.get_argument("tradetype", 0))   # 默認所有的數據都要加載
        page = (int)(self.get_argument("page", 1))
        limit = (int)(self.get_argument("limit", 100))
        finished = (self.get_argument("ext", None))   # 是否只加载已完成

        ret = None
        try:
            ret = SVC_TradeRecode.get_recode_list(u_id, type, page, limit, cid=c_id, finished=finished)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode = RET.RET_SERVERERR,
                errmsg = RETMSG_MAP[RET.RET_SERVERERR]
            ))
            return

        self.write(dict(
            errcode = RET.RET_OK,
            errmsg = RETMSG_MAP[RET.RET_OK],
            retdata = ret
        ))


class RevokeStockHandler(BaseHandler):
    """
    委托撤单。
    """
    @required_login
    def post(self, *args, **kwargs):
        """

        :return:
        """
        u_id = int(self.get_argument("uid"))
        id = (int)(self.get_argument("id"))

        try:
            SVC_TradeRecode.revoke_order(u_id, id)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode = RET.RET_SERVERERR,
                errmsg = RETMSG_MAP[RET.RET_SERVERERR]
            ))
            return


        self.write(dict(
            errcode = RET.RET_OK,
            errmsg = ""
        ))


class ListOrder(BaseHandler):
    """
    列出委托单.
    """
    @required_login
    def get(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        u_id = (int)(self.get_argument("uid"))
        c_id = (int)(self.get_argument("cid", 0))
        trade_type = self.get_argument("type", None)
        page = (int)(self.get_argument("page", 1))
        count = (int)(self.get_argument("count", 40))
        finished = self.get_argument("ext", None)

        res = []
        try:
            res = SVC_TradeRecode.list_orders(
                uid=u_id, cid=c_id, type=trade_type, page=page, count=count, finished=finished)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))

        logging.debug(res)
        self.write(dict(
            errcode=RET.RET_OK,
            errmsg=RETMSG_MAP[RET.RET_OK],
            retdata=res
        ))

def main():
    pass


if __name__ == '__main__':
    main()