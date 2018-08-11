#coding=utf-8

from handlers import userinfo
from handlers import verify_code
from handlers import favorite_stocks


urls = [
    (r'/api/login', userinfo.LoginHandler),
    (r'/api/logout', userinfo.LogoutHandler),
    (r'/api/register', userinfo.RegisterHanler),
    (r'/api/getuserinfo', userinfo.GetUserInfo),

    (r'/piccode', verify_code.PicCodeHandler),
    (r'/api/checkpic', verify_code.SMSCodeHandler),

    (r'/api/addstock2favorite', favorite_stocks.AddStock2FavoriteHandler),
    (r'/api/delstockfromfavorite', favorite_stocks.DelStockHandler),
    (r'/api/checkstockinfavorite', favorite_stocks.CheckStockHandler),
    (r'/api/getfavoritestocklist', favorite_stocks.GetStockListHandler),
]

def main():
    pass


if __name__ == '__main__':
    main()