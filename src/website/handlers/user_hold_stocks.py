#coding=utf-8

import logging
from utils.commons import required_login

from utils.response_code import RET, RETMSG_MAP
from handlers.basehandler import BaseHandler

from handlers.services.svc_user_hold_stocks import SVC_UserStocks

class GetStockList(BaseHandler):
    """
    獲取用戶的持倉股數
    """
    @required_login
    def get(self, *args, **kwargs):
        """
        獲取uid 根據uid獲取持倉股票信息
        :return:
        if success return [{'uid':xxx, 'code':xxx ...}, {...}]
        otherwise return ERR code and errmsg
        """

        u_id = self.get_argument("uid")

        res = None
        try:
            res = SVC_UserStocks.get_stock_list(u_id)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            return

        self.write(dict(
            errcode=RET.RET_OK,
            errmsg="",
            retdata = res
        ))



def main():
    pass


if __name__ == '__main__':
    main()