#coding=utf-8

import time

def Datetime2HowLong(strtime):
    """
    将一个时间转化为
    :param strtime: 一个字符串时间：格式 "%Y-%m-%d %H:%M:%S"
    :return:  as string, eg: 1分钟之前，1小时之前，etc...
    """
    now = time.time()
    ts_obj = time.strptime(strtime, "%Y-%m-%d %H:%M:%S")
    ts = time.mktime(ts_obj)

    dif = now - ts
    if (int)(dif / 31536000) > 0:
        return (str)((int)(dif / 31536000)) + "年"
    elif (int)(dif / 86400) > 0:
        return (str) ((int)(dif / 86400)) + "天"
    elif (int)(dif / 3600) > 0:
        return (str) ((int)(dif / 3600))+"小时"
    elif (int)(dif / 60) > 0:
        return (str) ((int)(dif / 60))+"分钟"
    else:
        return "刚刚"




####### test
##
def test_Datetime2HowLong():
    print(Datetime2HowLong('2018-08-14 19:19:08'))
    print(Datetime2HowLong('2018-10-13 15:37:08'))
    print(Datetime2HowLong('2018-10-12 15:37:08'))
    print(Datetime2HowLong('2018-9-13 15:37:08'))
    print(Datetime2HowLong('2010-10-13 15:38:08'))
    print(Datetime2HowLong('2018-10-13 15:40:08'))


def main():
    test_Datetime2HowLong()


if __name__ == '__main__':
    main()