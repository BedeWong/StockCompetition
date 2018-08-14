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
        u_id = self.get_argument("uid")
        stock_code = self.get_argument("code")
        stock_name = self.get_argument("name")
        stock_price = (float)(self.get_argument("price"))
        stock_amount = (int)(self.get_argument("amount"))

        try:
            SVC_TradeRecode.add_recode(u_id, 1, stock_price, stock_amount, stock_code, stock_name)
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

    """
    @required_login
    def post(self, *args, **kwargs):
        u_id = self.get_argument("uid")
        stock_code = self.get_argument("code")
        stock_name = self.get_argument("name")
        stock_price = (float)(self.get_argument("price"))
        stock_amount = (int)(self.get_argument("amount"))

        try:
            SVC_TradeRecode.add_recode(u_id, 2, stock_price, stock_amount, stock_code, stock_name)
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
        u_id = self.get_argument("uid")
        type = (int)(self.get_argument("tradetype", 0))   # 默認所有的數據都要加載
        page = (int)(self.get_argument("page", 1))
        limit = (int)(self.get_argument("limit", 40))
        finished = (self.get_argument("ext", 'all'))   # inished 只加載已完成   unfinished 只加載未完成 all 加載所有

        ret = None
        try:
            ret = SVC_TradeRecode.get_recode_list(u_id, type, page, limit, finished)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode = RET.RET_SERVERERR,
                errmsg = RETMSG_MAP[RET.RET_SERVERERR]
            ))
            return

        self.write(dict(
            errcode = RET.RET_OK,
            errmsg = RETMSG_MAP[RET.RET_SERVERERR],
            retdata = ret
        ))


class InvokeStockHandler(BaseHandler):
    """

    """
    @required_login
    def post(self, *args, **kwargs):
        """

        :return:
        """
        u_id = self.get_argument("uid")
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


def main():
    pass


if __name__ == '__main__':
    main()