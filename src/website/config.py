#coding=utf-8

import os

# redis 配置
redis_opt = {
    "host" : "120.79.208.53",
    "port" : "6379",
    "password" : "wong"
}

# 数据库链接
mysql_opt = {
    "host": "120.79.208.53",
    "user" : "wong",
    "password" : "wong",
    "database" : "stockcontest"
}

# 日志配置
log_path = os.path.join(os.path.dirname(__file__), "logs/log.log")
log_level = "debug"

# Appp配置参数
settings = {
    "debug" : True,
    "cookie_secret" : "FhLXI+BRRomtuaG47hoXEg3JCdi0BUi8vrpWmoxaoyI=",
    # "xsrf_cookies" : True
}

def main():
    pass


if __name__ == '__main__':
    main()