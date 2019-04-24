#coding=utf-8

import logging
from utils.commons import required_login

from utils.response_code import RET, RETMSG_MAP
from handlers.basehandler import BaseHandler
from handlers.services.svc_contest import SVC_Contest

from config import upload_path

import os
from datetime import datetime

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
        money = (int)(self.get_argument("money"))

        # 沒上傳文件的用默認的logo，
        # 上傳了得存起來，生成一個md5的文件名
        logo_name = None

        files = self.request.files.get('logo', None)
        if not files:
            logging.debug("no logo.")
        else:
            logo = files[0]
            content_type = logo['content_type']

            if content_type in ["image/gif", "image/jpeg",  'image/png']:
                logo_name = logo['filename']
                img_path = os.path.join(upload_path, logo_name)

                with open(img_path, 'wb') as f:
                    f.write(logo['body'])

        if len(title) < 2 or starttm > endtm or money not in [50, 100, 500, 1000]:
            logging.info("ContestCreate:%s, %s-%s, money:%s", title, starttm, endtm, money)
            self.write(dict(
                errcode=RET.RET_PARAMERR,
                errmsg=RETMSG_MAP[RET.RET_PARAMERR]
            ))
            return

        now = datetime.now().strftime("%y-%m-%d")

        if starttm <= now :
            logging.info("starttm <= endtm: %s-%s", starttm, endtm)
            self.write(dict(
                errcode=RET.RET_PARAMERR,
                errmsg=RETMSG_MAP[RET.RET_PARAMERR]
            ))
            return

        try:
            if datetime.strptime(starttm, '%Y-%m-%d') and datetime.strptime(endtm, '%Y-%m-%d'):
                pass
            else:
                logging.info("time 格式錯誤:", starttm, endtm)
                self.write(dict(
                    errcode=RET.RET_PARAMERR,
                    errmsg=RETMSG_MAP[RET.RET_PARAMERR]
                ))
                return
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_PARAMERR,
                errmsg=RETMSG_MAP[RET.RET_PARAMERR]
            ))
            return

        contest = None
        try:
            contest = SVC_Contest.add_contest(u_id, title, desc, starttm, endtm, money, logo_name)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_PARAMERR,
                errmsg=RETMSG_MAP[RET.RET_PARAMERR]
            ))
            return


        #####  ok
        self.write(dict(
            errcode=RET.RET_OK,
            errmsg="創建成功！",
            retdata = contest.to_json() if contest  else []
        ))

        logging.debug("ContestCreate: title:%s, desc:%s, uid:%s, starttm:%s, endtm:%s", title, desc, u_id, starttm, endtm)



class ContestJoin(BaseHandler):
    """
    用戶加入比賽
    """

    @required_login
    def post(self, *args, **kwargs):
        """

        :return:
        """

        u_id = self.get_argument("uid")
        contestid = (int)(self.get_argument("contestid"))

        try:
            SVC_Contest.join_contest(u_id, contestid)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            return

        #####  ok
        self.write(dict(
            errcode=RET.RET_OK,
            errmsg="加入成功！"
        ))

class ContestQuit(BaseHandler):
    """
    用戶退出比賽
    """
    @required_login
    def post(self, *args, **kwargs):
        """

        :return:
        """

        u_id = self.get_argument("uid")
        id = self.get_argument("id")

        try:
            SVC_Contest.quite_contest(u_id, id)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            return

        self.write(dict(
            errcode=RET.RET_OK,
            errmsg=""
        ))

class Contest_get_list(BaseHandler):
    """
    獲取比賽列表
    """

    def get(self, *args, **kwargs):
        """
        獲取比賽的列表：
        page:
        count:
        :return:
        """

        page = int(self.get_argument("page", 0))
        count = int(self.get_argument("count", 40))

        logging.debug('param: page: %d, count: %d' % (page, count))
        res = None
        try:
            res = SVC_Contest.get_contest_list(page, count)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            return

        if not res:
            res = []

        #####  ok
        self.write(dict(
            errcode=RET.RET_OK,
            errmsg="",
            retdata = res
        ))

class Contest_get_user_contest(BaseHandler):
    """
    獲取用戶參加了得比賽
    """

    @required_login
    def get(self, *args, **kwargs):
        """
        uid;
        all: boolean  是否獲取全部（包含已結束的比賽）
        :return:
        """

        u_id = self.get_argument("uid");
        all = self.get_argument('all', False)

        res = None
        try:
            res = SVC_Contest.get_user_contest_list(u_id, all)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            return

        if not res:
            res = []

        #####  ok
        self.write(dict(
            errcode=RET.RET_OK,
            errmsg="",
            retdata = res
        ))


class Contest_get_contest_rank(BaseHandler):
    """
    獲取用戶比賽的列表排名
    """

    @required_login
    def get(self, *args, **kwargs):
        """

        :return:
        """

        contestid = self.get_argument("id")
        page = self.get_argument("page", 0)
        count = self.get_argument("count", 20)

        res = None
        try:
            res = SVC_Contest.get_contest_detail_rank_users(contestid, page, count)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            return

        self.write(dict(
            errcode=RET.RET_OK,
            errmsg="",
            retdata = res
        ))

class Contest_check_in_contest(BaseHandler):
    """

    """
    @required_login
    def get(self, *args, **kwargs):
        """
        檢查用戶是否在比賽中：0 可加入  1 已加入 2 已退出
        :return:
        """

        uid = self.get_argument("uid")
        id = self.get_argument("id")

        ret = 0
        try:
            ret = SVC_Contest.check_user_in_contest(uid, id)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            return

        self.write(dict(
            errcode=RET.RET_OK,
            errmsg="",
            retdata = ret
        ))

class ContestUserInfo(BaseHandler):
    """
    獲取用戶的比賽信息數據：
    """
    @required_login
    def get(self, *args, **kwargs):
        """
        id:
        cid:
        :return:
        """
        uid = self.get_argument("uid")
        cid = self.get_argument("cid")

        if not all([id, cid]):
            logging.error("參數錯誤:" + cid + "" + uid)
            self.write(dict(
                errcode=RET.RET_PARAMERR,
                errmsg=RETMSG_MAP[RET.RET_PARAMERR]
            ))
            return

        res = None
        try:
            res  = SVC_Contest.get_contest_user_info(uid, cid)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            return

        self.write(dict(
            errcode=RET.RET_OK,
            errmsg="",
            retdata = res
        ))


def main():
    pass


if __name__ == '__main__':
    main()