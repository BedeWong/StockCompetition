#coding=utf-8

from utils.response_code import RET, RETMSG_MAP
from utils.commons import required_login
from handlers.services.svc_favorite_stocks import SVC_FavoriteStocks

from handlers.basehandler import BaseHandler

import logging
import  traceback

class AddStock2FavoriteHandler(BaseHandler):
    """
    處理用戶添加自選股請求
    """

    @required_login
    def post(self, *args, **kwargs):
        """
        u_id： 用戶id
        s_stock_code：股票代碼，如：sh603036
        :return:
        """
        u_id = self.get_argument("uid")
        s_stock_code = self.get_argument("code")
        s_stock_name = self.get_argument("name")

        logging.debug("添加自選股：", u_id, s_stock_code, s_stock_name)

        try:
            ret = SVC_FavoriteStocks.add_stock(u_id, s_stock_code, s_stock_name)
        except Exception as e:
            traceback.print_exc()
            logging.error(e)

            self.write(dict(
                errcode = RET.RET_SERVERERR,
                errmsg = RETMSG_MAP[RET.RET_SERVERERR]
            ))

        if ret == 'exist' :
            self.write(dict(
                errcode=RET.RET_OK,
                errmsg="已經添加，無需再次添加！"
            ))
        else:
            self.write(dict(
                errcode=RET.RET_OK,
                errmsg="添加成功！"
            ))

class CheckStockHandler(BaseHandler):
    """
    檢測股票是否在自選股列表
    """

    @required_login
    def post(self, *args, **kwargs):
        """
        uid: user id
        s_stock_code: 股票代碼
        :return:
        """
        u_id = self.get_argument('uid')
        s_stock_code = self.get_argument("code")

        logging.debug("check自選股：", u_id, s_stock_code)

        try:
            ret = SVC_FavoriteStocks.check_stock(u_id, s_stock_code)
        except Exception as e:
            traceback.print_exc()
            logging.error(e)

            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))

        self.write(dict(
            errcode=RET.RET_OK,
            retdata = {"ret":ret}
        ))

class DelStockHandler(BaseHandler):
    """
    從自選列表刪除
    """

    @required_login
    def post(self, *args, **kwargs):
        """
        uid: user id
        s_stock_code: 股票代碼
        :return:
        """
        u_id = self.get_argument('uid')
        s_stock_code = self.get_argument("code")

        logging.debug("check自選股：", u_id, s_stock_code)

        try:
            SVC_FavoriteStocks.del_stock(u_id, s_stock_code)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode = RET.RET_SERVERERR,
                errmsg = RETMSG_MAP[RET.RET_SERVERERR]
            ))

        self.write(dict(
            errcode=RET.RET_OK
        ))

class GetStockListHandler(BaseHandler):
    """獲取用戶自選股列表數據"""

    def get(self, *args, **kwargs):
        """
        uid
        :return:
        """

        u_id = self.get_argument("uid")

        try:
            res = SVC_FavoriteStocks.get_stocks(u_id)
        except Exception as e:
            traceback.print_exc()
            logging.error(e)

            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))

        logging.debug(res)

        self.write(dict(
            errcode = RET.RET_OK,
            retdata  = res
        ))

def main():
    pass


if __name__ == '__main__':
    main()