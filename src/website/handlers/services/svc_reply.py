#coding=utf-8

from handlers.models.basemodel import dbsession
from sqlalchemy import and_, or_, desc
from sqlalchemy.orm.exc import NoResultFound

from handlers.models.tb_reply import Reply
from handlers.models.tb_article import Article
from handlers.models.tb_reply_upcounts import ReplyUpcounts

from datetime import datetime
import datetime as dttm

class SVC_Reply(object):
    """
    回復相關處理
    """

    @staticmethod
    def addReply(uid, aid, content):
        """
        添加一個回復
        :param uid:
        :param aid:
        :return:
        """

        reply = Reply()
        reply.u_id = uid
        reply.a_id = aid
        reply.r_content = content

        try:
            dbsession.add(reply)
            dbsession.commit()
        except Exception as e:
            dbsession.rollback()
            raise e


    @staticmethod
    def delReply(uid, rid):
        """
        刪除一個評論
        :param uid:
        :param rid:
        :return:
        """

        recode = None
        try:
            recode = dbsession.query(Reply).filter(and_(Reply.id==rid, Reply.u_id==uid)).one()
        except NoResultFound as e:
            raise e
        except Exception as e:
            dbsession.rollback()
            raise e

        if recode:
            try:
                recode.r_status = 1
                dbsession.merge(recode)
                dbsession.commit()

                ### 這個回復是回復的話題，  所有在此回復上的回復消息 都應該刪除
                if recode.r_reply_id == 0:
                    dbsession.query(Reply).filter(Reply.r_reply_id == recode.id).update({Reply.r_status : 1})
                    dbsession.commit()
            except Exception as e:
                dbsession.rollback()
                raise e

    @staticmethod
    def addReplyReply(uid, aid, rid, content):
        """
        回復別人的回復消息
        :param uid:
        :param aid:
        :param rid:
        :return:
        """

        reply = Reply()
        reply.r_reply_id = rid
        reply.u_id = uid
        reply.a_id = aid
        reply.r_content = content
        try:
            dbsession.add(reply)
            dbsession.commit()
        except Exception as e:
            dbsession.rollback()
            raise e


    @staticmethod
    def getReplyByArticleId(aid, page=0, count=40):
        """
        獲取話題的回復
        :param aid:
        :return:
        """

        res = None
        try:
            res = dbsession.query(Reply).filter(Reply.a_id == aid).limit(count).offset(count*page).all()
        except Exception as e:
            dbsession.rollback()
            raise e

        if not res:
            return []

        lst = []
        for it in res:
            lst.append(it.to_json())

        return lst

    @staticmethod
    def getNewestReply(page=0, count=40):
        """
        獲取最新的回復消息
        :param page:
        :param count:
        :return: 返回dict， 包括回復相關的所有數據和話題標題，話題作者
        """

        res = None
        try:
            res = dbsession.query(Reply, Article).join(Article, Article.id==Reply.a_id).order_by(desc(Reply.r_time)).limit(count).offset(page*count) \
                .all()
        except Exception as e:
            dbsession.rollback()
            raise e

        if not res:
            return []

        lst = []
        for it in res:
            tmp = it[0].to_json()
            tmp.update(it[1].to_json())
            lst.append(tmp)

        return lst

    @staticmethod
    def upcountReply(uid, rid):
        """
                給評論點贊, 如果電讚了得  就取消點讚
                :param id:
                :param uid:
                :return:
                """

        recode = None
        try:
            recode = dbsession.query(ReplyUpcounts).filter(
                and_(ReplyUpcounts.r_id == rid, ReplyUpcounts.u_id == uid)).one()
        except NoResultFound as e:
            pass
        except Exception as e:
            dbsession.rollback()
            raise e

        if not recode:
            recode = ReplyUpcounts()
            recode.u_id = uid
            recode.r_id = rid
            try:
                dbsession.add(recode)
                dbsession.commit()
            except Exception as e:
                dbsession.rollback()
                raise e

            try:
                dbsession.query(Reply).filter(Reply.id == rid).update({Reply.r_upcounts: Reply.r_upcounts + 1})
                dbsession.commit()
            except Exception as e:
                dbsession.rollback()
                raise e

        else:
            try:
                dbsession.delete(recode)
                dbsession.commit()
                dbsession.query(Reply).filter(Reply.id == rid).update({Reply.r_upcounts: Reply.r_upcounts - 1})
                dbsession.commit()
            except Exception as e:
                dbsession.rollback()

    @staticmethod
    def checkUpcount(uid, rid):
        """
        檢查是否是點過讚了
        :param uid:
        :param rid:
        :return:  True  or False
        """

        recode = None
        try:
            dbsession.query(ReplyUpcounts).filter(
                and_(ReplyUpcounts.r_id == rid, ReplyUpcounts.u_id == uid)).one()
        except NoResultFound as e:
            return False
        # except Exception as e:
        #     raise e

        if recode:
            return True
        return False  # 沒有點過


################  test
######

import traceback
def test_add():
    try:
        SVC_Reply.addReply("27052237", 2, "這是一條評論")
        SVC_Reply.addReply("27052245", 2, "這是一條評論")
        SVC_Reply.addReply("27052237", 5, "這是一條評論")
        SVC_Reply.addReply("27052245", 3, "這是一條評論")
        SVC_Reply.addReply("27052245", 3, "這是一條評論")
    except Exception as e:
        traceback.print_exc()

def test_del():
    SVC_Reply.delReply('27052245', 4)

def test_addrreply():
    try:
        SVC_Reply.addReplyReply('27052245', 2, 1, "評論了一條評論")
    except Exception as e:
        traceback.print_exc()

def test_getArticleReply():
    try:
        print(SVC_Reply.getReplyByArticleId(2))
    except Exception as e:
        traceback.print_exc()

def get_newest():
    try:
        print(SVC_Reply.getNewestReply())
    except Exception as e:
        traceback.print_exc()



def main():
    # test_add()
    # test_del()
    # test_addrreply()
    test_getArticleReply()
    get_newest()


if __name__ == '__main__':
    main()