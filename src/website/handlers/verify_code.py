#coding=utf-8

from handlers.basehandler import BaseHandler
from utils.contansts import VERIFY_CODE_EXPIRES_SECONDS
from libs.captcha_gen import CaptchaGen
from utils.response_code import RET, RETMSG_MAP
from libs.aliyun_sms_code import Send_SMS

import random
import logging
import re
import uuid

class PicCodeHandler(BaseHandler):

    def get(self):

        # 生成一个验证码，
        cap = CaptchaGen()
        name, text, imgdata = cap.createNew()

        self.set_cookie("cur_pic", name)
        try:
            logging.debug(name)
            logging.debug(text)
            self.redis.set("pic_code_%s" % name, text.lower(), VERIFY_CODE_EXPIRES_SECONDS)
        except Exception as e:
            logging.error(e)
            raise e

        self.set_header("Content-Type", "image/png")
        self.write(imgdata)

class SMSCodeHandler(BaseHandler):
    """"""

    def post(self):
        cur_pic = self.get_cookie("cur_pic", None)
        # pic_code = self.get_argument("piccode")
        # phone = self.get_argument("mobile")
        pic_code = self.json_args.get('piccode')
        phone = self.json_args.get('mobile')

        logging.debug("cookie:cur_pic: %s" % cur_pic)
        logging.debug("pic_code: %s" % pic_code)
        logging.debug("phone: %s" % phone)
        # 验证参数
        if not all((cur_pic, pic_code, phone)):
            self.write(dict(
                errcode = RET.RET_PARAMERR,
                errmsg = RETMSG_MAP[RET.RET_PARAMERR]
            ))
            return

        ## 获取验证码
        real_sms_code = None
        try:
            real_sms_code = self.redis.get("pic_code_%s" % cur_pic)
            # self.redis.delete("pic_code_%s" % cur_pic)   # 删除掉
        except Exception as e:
            logging.error(e)
            raise e

        if real_sms_code.decode() != pic_code.lower():
            self.write(dict(
                errcode=RET.RET_PICCODEERR,
                errmsg=RETMSG_MAP[RET.RET_PICCODEERR]
            ))
            return

        ### 验证手机 号码
        if not re.match(r"^1[0-9]{10}$", phone):
            return self.write(dict(
                errcode=RET.RET_MOBILEPHONEERR,
                errmsg=RETMSG_MAP[RET.RET_MOBILEPHONEERR]
            ))

        ### 生成短信码
        sms_code = ''.join( random.sample('0123456789', 6) )
        # 不使用uuid作为表示，可以直接使用手机号码
        # uuid_code = uuid.uuid4().hex
        try:
            self.redis.set("smscode_%s" % phone, sms_code, VERIFY_CODE_EXPIRES_SECONDS)
        except Exception as e:
            logging.error(e)
            raise e

        #### 发送短信
        __business_id = uuid.uuid1()
        params = '{"code":%s,"product":"注册"}' % sms_code
        result = Send_SMS.send_sms(__business_id, phone, "Matchs", "SMS_135600035", params)
        if r'"Code":"OK"' not in result.decode():
            logging.error(result)
            logging.exception(str(result))
            return self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))

        return self.write(dict(
            errcode = RET.RET_OK,
            errmsg = RETMSG_MAP[RET.RET_OK]
        ))

def main():
    pass


if __name__ == '__main__':
    main()