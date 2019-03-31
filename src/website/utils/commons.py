#coding=utf-8

import functools
from utils.response_code import RET, RETMSG_MAP

def required_login(func):
    @functools.wraps(func)
    def wrapper(request_obj, *args, **kwargs):
        # 调用get_current_user方法判断用户是否登录
        if not request_obj.get_current_user():
            return request_obj.write( dict(errcode=RET.RET_NOTLOGIN, errmsg=RETMSG_MAP[RET.RET_NOTLOGIN]) )
        return func(request_obj, *args, **kwargs)
    return wrapper

def main():
    pass


if __name__ == '__main__':
    main()