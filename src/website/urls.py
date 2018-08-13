#coding=utf-8

from handlers import userinfo
from handlers import verify_code
from handlers import favorite_stocks
from handlers import user_stocks
from handlers import trade_recode

urls = [
    (r'/api/login', userinfo.LoginHandler),
    (r'/api/logout', userinfo.LogoutHandler),
    (r'/api/register', userinfo.RegisterHanler),
    (r'/api/getuserinfo', userinfo.GetUserInfo),

    (r'/piccode', verify_code.PicCodeHandler),
    (r'/api/checkpic', verify_code.SMSCodeHandler),

    # 用戶自選股
    (r'/api/addstock2favorite', favorite_stocks.AddStock2FavoriteHandler),
    (r'/api/delstockfromfavorite', favorite_stocks.DelStockHandler),
    (r'/api/checkstockinfavorite', favorite_stocks.CheckStockHandler),
    (r'/api/getfavoritestocklist', favorite_stocks.GetStockListHandler),

    # 持倉股票
    (r'/api/getholdstocklist', user_stocks.GetStockList),

    # 股票交易記錄相關
    (r'/api/buystock', trade_recode.BuyStockHander),
    (r'/api/salestock', trade_recode.SaleStockHandler),
    (r'/api/gettradehistory', trade_recode.GetTradeHistoryHandler),
    (r'/api/invokestock', trade_recode.InvokeStockHandler),
]

def main():
    pass


if __name__ == '__main__':
    main()