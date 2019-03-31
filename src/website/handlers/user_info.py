#coding=utf-8

import re
import hashlib
import logging

from utils.commons import required_login

from utils.response_code import RET, RETMSG_MAP
from handlers.basehandler import BaseHandler
from handlers.services.svc_userinfo import SVC_userinfo


class LoginHandler(BaseHandler):
    """

    """
    def post(self, *args, **kwargs):
        """
        可以使用用户名、手机号、邮箱进行登录
        :param args:
        :param kwargs:
        :return:
        """

        # 判断目前是不是已经登录的用户
        session_data = self.get_current_user()
        if session_data:
            pass

        logging.debug(self.request.body)
        loginid = self.get_argument("loginId")
        pwd     = self.get_argument("password")
        logging.debug(loginid + ", " + pwd)

        if not all([loginid, pwd]):
            return self.write(dict(errcode=RET.RET_PARAMERR, errmsg=RETMSG_MAP[RET.RET_PARAMERR]))

        user = None
        try:
            # 邮箱登录
            if '@' in loginid:
                user = SVC_userinfo.get_user_byemail(loginid)

            # 手机号登录
            elif re.match(r'^1[0-9]{10}$', loginid):
                user = SVC_userinfo.get_user_bymobile(loginid)

            # 用户名登录
            else:
                user = SVC_userinfo.get_user_byname(loginid)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_DBERR,
                errmsg="用户名或密码错误！"
            ))
            return

        md5 = hashlib.md5()
        if isinstance(pwd, str):
            pwd = pwd.encode('utf8')
        md5.update(pwd)
        pwdmd5 = md5.hexdigest()

        if user.u_passwd != pwdmd5:
            self.write(dict(
                errcode = RET.RET_UIDORPWDERR,
                errmsg  = RETMSG_MAP[RET.RET_UIDORPWDERR]
            ))
            return

        # 查看redis中是否含有本账户的数据，清除掉，防止多地登录
        try:
            userid = user.id
            res = self.redis.hget("tb_users", "uid:%d" % userid)
            if res:
                logging.debug(res)
                self.session.clear_session(res, userid)
                logging.debug("tb_users hset uid:%d" % userid)
            self.redis.hset("tb_users", "uid:%d" % userid, self.session._session_id)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            return

        # 保存session到redis
        user_json_data = user.to_dict()
        self.session.data.update(user_json_data)
        self.session.save()

        self.write(dict(
            errcode = RET.RET_OK,
            errmsg  = "",
            token  = self.session._session_id,
            retdata = user_json_data
        ))

        logging.info(self.session._session_id)
        logging.info(user_json_data)


class LogoutHandler(BaseHandler):
    """

    """

    @required_login
    def get(self):
        self.session.clear()
        return self.write(dict(
            errcode = RET.RET_OK,
            errmsg  = "登出成功"
        ))


class RegisterHanler(BaseHandler):
    """"""
    def post(self):
        uname = self.get_argument('uname')
        usex = self.get_argument("usex", 0)
        uaddress = self.get_argument("uaddress")
        uemail = self.get_argument("uemail")
        umobile  = self.get_argument("mobile")
        upwd     = self.get_argument("pwd")

        sms_code = self.get_argument("smscode")
        real_sms_code = None
        try:
            real_sms_code = self.redis.get("smscode_%s" % umobile)
        except Exception as e:
            logging.error(e)
            return self.write(dict(
                errcode=RET.RET_DBERR,
                errmsg="服务器错误！"
            ))

        if not real_sms_code:
            return self.write(dict(
                errcode=RET.RET_SMSCODETIMEOUT,
                errmsg = RETMSG_MAP[RET.RET_SMSCODETIMEOUT]
            ))

        logging.debug("smscode=%s, ss_code=%s" % (sms_code, real_sms_code))
        if sms_code != real_sms_code:
            return self.write(dict(
                errcode = RET.RET_SMSCODEERR,
                errmsg = RETMSG_MAP[RET.RET_SMSCODEERR]
            ))

        pwd = hashlib.md5().update(upwd.encode('utf8')).hexdigest()
        SVC_userinfo.add_user(u_name=uname,
                              u_sex = usex,
                              # u_address = usex,
                              u_email = uemail,
                              u_mobilephone = umobile,
                              u_pwd = pwd
                              )


class GetUserInfo(BaseHandler):
    """用於檢測用戶的token是否過期，過期返回錯誤碼，未過期返回用戶數據"""

    @required_login
    def post(self):

        data = self.get_current_user()
        logging.debug("GetUserInfo:data type:%s data:%s" % (type(data), data))
        self.write(dict(
                errcode=RET.RET_OK,
                errmsg="",
                token=self.session._session_id,
                retdata=data
            ))



class UserInfo(BaseHandler):
    """
    获取用户的信息。
    """

    def get(self, userid):
        """
        userid： 匹配到的用户id
        :return:
        """

        res = None
        try:
            res = SVC_userinfo.get_user_byid((int)(userid))
        except Exception as e:
            logging.error(e)
            return self.write(dict(
                errcode=RET.RET_SMSCODEERR,
                errmsg=RETMSG_MAP[RET.RET_SMSCODEERR]
            ))

        self.write(dict(
            errcode=RET.RET_OK,
            errmsg="",
            retdata= res.to_dict()
        ))

def main():
    pass


if __name__ == '__main__':
    main()