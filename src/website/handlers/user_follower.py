#coding=utf-8
import logging
from utils.commons import required_login

from utils.response_code import RET, RETMSG_MAP
from handlers.basehandler import BaseHandler
from handlers.services.svc_user_follower import SVC_UserFollower

class FollowerRelationAdd(BaseHandler):
    """
    用戶關注： uid 關注 fuid
    """

    @required_login
    def post(self, *args, **kwargs):
        """
        uid:
        fuid：
        :return:
        """

        uid = self.get_argument("uid")
        fuid = self.get_argument("fuid")

        checked = False
        try:
            checked = SVC_UserFollower.check_user_folower_relation(uid, fuid)
            if not checked:
                SVC_UserFollower.add_recode(uid, fuid)
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


class FollowerRelationDel(BaseHandler):
    """
    取關: uid 取关 fuid
    """
    @required_login
    def post(self, *args, **kwargs):
        """
        uid:
        fuid:
        :return:
        """
        uid = self.get_argument("uid")
        fuid = self.get_argument("fuid")

        try:
            SVC_UserFollower.del_recode(fuid, uid)
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

class GetFollowersCount(BaseHandler):
    """
    獲取用戶的粉絲數
    """

    @required_login
    def get(self, *args, **kwargs):
        """
        uid:
        :return:
        """

        uid = self.get_argument("uid")

        res = None
        try:
            res = SVC_UserFollower.get_user_followers_count(uid)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            return

        if not res:
            res = 0

        rdat = {"count":res}  # dict

        self.write(dict(
            errcode=RET.RET_OK,
            errmsg="",
            retdata = rdat
        ))


class CheckUserFollowerRelation(BaseHandler):
    """
    檢測fuid是不是uid關注的人
    """

    @required_login
    def post(self, *args, **kwargs):
        """
        uid:
        :return:
        """

        uid = self.get_argument("uid")
        fuid = self.get_argument("fuid")
        ret = None
        try:
            ret = SVC_UserFollower.check_user_folower_relation(fuid, uid)
        except Exception as e:
            logging.error(e)
            self.write(dict(
                errcode=RET.RET_SERVERERR,
                errmsg=RETMSG_MAP[RET.RET_SERVERERR]
            ))
            return

        if not ret:
            ret = False

        rdat = {"check": ret}  # dict

        self.write(dict(
            errcode=RET.RET_OK,
            errmsg="",
            retdata = rdat
        ))



def main():
    pass


if __name__ == '__main__':
    main()