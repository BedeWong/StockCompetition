#coding=utf-8

class RET:
    RET_OK          = "0"
    RET_DBERR       = "4001"
    RET_NOTLOGIN    = "4002"
    RET_PARAMERR    = "4003"
    RET_UIDORPWDERR = "4004"
    RET_SMSCODEERR  = "4005"
    RET_SMSCODETIMEOUT = "4006"
    RET_PICCODEERR     = "4007"
    RET_MOBILEPHONEERR = "4008"
    RET_SERVERERR      = "4009"



RETMSG_MAP = {
    RET.RET_OK      : "OK",
    RET.RET_DBERR   : "数据库错误",
    RET.RET_NOTLOGIN: "请登录",
    RET.RET_PARAMERR: "参数错误",
    RET.RET_UIDORPWDERR: "用户名或密码错误",
    RET.RET_SMSCODEERR : "手机验证码错误",
    RET.RET_SMSCODETIMEOUT : "手机验证码过期",
    RET.RET_PICCODEERR  : "图片验证码错误",
    RET.RET_MOBILEPHONEERR : "请输入正确的手机号",
    RET.RET_SERVERERR     : "服务器错误"
}