#coding=utf-8

import logging
from utils.commons import required_login

from utils.response_code import RET, RETMSG_MAP
from handlers.basehandler import BaseHandler
from handlers.services.svc_contest_user_hold_stocks import SVC_UserStocks
from handlers.services.svc_trade_recode import SVC_TradeRecode

class ListUserContestStocks(BaseHandler):
    """
    获取用户比赛持仓股
    """

    @required_login
    def get(self, *args, **kwargs):
        """

        :return:
        """
        uid = self.get_argument("uid")
        cid = int(self.get_argument("cid"))
        page = (int)(self.get_argument("page", 0))
        count = (int)(self.get_argument("count", 20))

        logging.debug("uid:%s, cid:%s, page:%d, count:%d", uid, cid, page, count)
        res = None
        try:
            res = SVC_UserStocks.get_stock_list(uid, cid, page, count)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            return

        logging.debug("reult:%s", res)
        self.write(dict(
            errcode=RET.RET_OK,
            errmsg="",
            retdata=res
        ))


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
        c_id = int(self.get_argument("cid"))
        stock_code = self.get_argument("code")
        stock_name = self.get_argument("name")
        stock_price = (float)(self.get_argument("price"))
        stock_amount = (int)(self.get_argument("amount"))

        try:
            SVC_TradeRecode.add_order(u_id, 1, stock_price, stock_amount, stock_code, stock_name, c_id)
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
        u_id = (int)(self.get_argument("uid"))
        c_id = (int)(self.get_argument("cid"))
        stock_code = self.get_argument("code")
        stock_name = self.get_argument("name")
        stock_price = (float)(self.get_argument("price"))
        stock_amount = (int)(self.get_argument("amount"))

        try:
            SVC_TradeRecode.add_order(u_id, 2, stock_price, stock_amount, stock_code, stock_name, c_id)
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
        u_id = int(self.get_argument("uid"))
        c_id = int(self.get_argument("cid"))
        type = (int)(self.get_argument("tradetype", 0))   # 默認所有的數據都要加載
        page = (int)(self.get_argument("page", 0))
        limit = (int)(self.get_argument("limit", 40))
        finished = (self.get_argument("ext", 'all'))   # inished 只加載已完成   unfinished 只加載未完成 all 加載所有

        ret = None
        try:
            ret = SVC_TradeRecode.get_recode_list(u_id, c_id, type, page, limit)
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


class RevokeStockHandler(BaseHandler):
    """

    """
    @required_login
    def post(self, *args, **kwargs):
        """

        :return:
        """
        u_id = self.get_argument("uid")
        c_id = self.get_argument("cid")
        id = (int)(self.get_argument("id"))

        try:
            SVC_TradeRecode.revoke_order(u_id, c_id, id)
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