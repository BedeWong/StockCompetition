#coding=utf-8

from handlers import userinfo
from handlers import verify_code


urls = [
    (r'/api/login', userinfo.LoginHandler),
    (r'/api/logout', userinfo.LogoutHandler),
    (r'/api/register', userinfo.RegisterHanler),
    (r'/api/getuserinfo', userinfo.GetUserInfo),
    (r'/piccode', verify_code.PicCodeHandler),
    (r'/api/checkpic', verify_code.SMSCodeHandler),
]

def main():
    pass


if __name__ == '__main__':
    main()