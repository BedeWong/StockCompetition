#coding=utf-8

import logging
from utils.commons import required_login

from utils.response_code import RET, RETMSG_MAP
from handlers.basehandler import BaseHandler

from config import default_logo, upload_path

import os

class ContestCreate(BaseHandler):
    """
    比賽創建處理：
    """

    @required_login
    def post(self, *args, **kwargs):
        logging.debug(self.request.arguments)
        u_id = self.get_argument("uid")
        title = self.get_argument("title")
        desc = self.get_argument("desc")
        starttm = self.get_argument("starttm")
        endtm = self.get_argument("endtm")
        money = self.get_argument("money")

        files = self.request.files.get("logo", None)
        if not files:
            logo = default_logo
        else:
            logo = files[0]

            img_path = os.path.join(upload_path, logo['filename'])
            with open(img_path, 'wb') as f:
                f.write(logo['body'])

        logging.debug("ContestCreate: title:%s, desc:%s, uid:%s, starttm:%s, endtm:%s", title, desc, u_id, starttm, endtm)



def main():
    pass


if __name__ == '__main__':
    main()