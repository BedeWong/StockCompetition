#coding=utf-8

from handlers.models.basemodel import dbsession
from sqlalchemy import and_, or_
from sqlalchemy.orm.exc import NoResultFound

from handlers.models.tb_article import Article
from handlers.models.tb_article_upcounts import ArticleUpcounts

from datetime import datetime
import datetime as dttm

class SVC_Article(object):
    """
    对文章的 处理 类
    """

    @staticmethod
    def addArticle(uid, title, content):
        """
        添加一個話題
        :param uid:
        :param title:
        :param content:
        :return:
        """

        article = Article()
        article.u_id = uid
        article.a_title = title
        article.a_content = content

        try:
            dbsession.add(article)
            dbsession.commit()
        except Exception as e:
            dbsession.rollback()
            raise e


    @staticmethod
    def delArticle(uid, id):
        """
        刪除一個話題， 邏輯刪除
        :param uid:
        :param id:
        :return: None, throw exception if error
        """

        article = None
        try:
            article = dbsession.query(Article).filter(and_(Article.id==id, Article.u_id==uid)).one()
        except NoResultFound as e:
            return "話題找不到了。。。"
        except Exception as e:
            dbsession.rollback()
            raise e

        if  not article:
            return "話題找不到了。。。"

        article.a_status = 2      # 關閉（邏輯刪除）
        try:
            dbsession.merge(article)
            dbsession.commit()
        except Exception as e:
            dbsession.rollback()
            raise e

    @staticmethod
    def getArticleById(id):
        """
        獲取文章數據
        :param id:
        :return:
        """

        article = None
        try:
            article = dbsession.query(Article).filter(Article.id == id).one()
        except NoResultFound as e:
            raise e
        except Exception as e:
            dbsession.rollback()
            raise e

        if article:
            return article.to_json()

        return None


    @staticmethod
    def getNewestArticles(page=0, count=20):
        """
        按最新排序獲取，分頁
        :param page:
        :param count:
        :return:
        """

        res = None
        try:
            res = dbsession.query(Article).order_by('a_pub_time').limit(count).offset(page*count).all()
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
    def getArticleNewestHot(latest_day=7, page=0, count=20):
        """
        獲取熱門的文章：依據latest day 進行排序，查看數量最多的
        :param latest_day 時間區間，7表示最近一周的熱門話題
        :return:
        """

        res = None
        try:
            dt = datetime.today() - dttm.timedelta(latest_day)
            res = dbsession.query(Article).filter(Article.a_pub_time > dt).order_by(Article.a_interviews).limit(count).offset(page*count).all()
        except Exception as e:
            raise e

        if not res:
            return []

        lst = []
        for it in res:
            lst.append(it.to_json())

        return lst

    @staticmethod
    def getArticleByUid(uid, page=0, count=40):
        """
        獲取用戶發表的
        :param uid:
        :return:
        """

        res = None
        try:
            res = dbsession.query(Article).filter_by(u_id=uid).order_by('a_pub_time').limit(count).offset(page*count).all()
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
    def upcountArticle(aid, uid):
        """
        給文章點贊, 如果電讚了得  就取消點讚
        :param id:
        :param uid:
        :return:
        """

        recode = None
        try:
            recode = dbsession.query(ArticleUpcounts).filter(and_(ArticleUpcounts.a_id==aid, ArticleUpcounts.u_id == uid)).one()
        except NoResultFound as e:
            pass
        except Exception as e:
            dbsession.rollback()
            raise e

        if not recode:
            recode = ArticleUpcounts()
            recode.u_id = uid
            recode.a_id = aid
            try:
                dbsession.add(recode)
                dbsession.commit()
            except Exception as e:
                dbsession.rollback()
                raise e

            try:
                dbsession.query(Article).filter(Article.id == aid).update({Article.a_upcounts : Article.a_upcounts+1})
                dbsession.commit()
            except Exception as e:
                dbsession.rollback()
                raise e

        else:
            try:
                dbsession.delete(recode)
                dbsession.commit()
                dbsession.query(Article).filter(Article.id == aid).update({Article.a_upcounts: Article.a_upcounts - 1})
                dbsession.commit()
            except Exception as e:
                dbsession.rollback()


    @staticmethod
    def checkUpcount(uid, aid):
        """
        檢查是否是點過讚了
        :param uid:
        :param aid:
        :return:  True  or False
        """

        recode = None
        try:
            dbsession.query(ArticleUpcounts).filter(and_(ArticleUpcounts.a_id == aid, ArticleUpcounts.u_id == uid)).one()
        except NoResultFound as e:
            return False
        # except Exception as e:
        #     raise e

        if recode:
            return True
        return False     # 沒有點過



########  test
###
import  traceback

def test_add():
    try:
        SVC_Article.addArticle("27052237", "測試標題1", "測試一下啦， 内容要點寫，我都唔知講D咩好")
        SVC_Article.addArticle("27052237", "測試標題2", "測試一下啦， 内容要點寫，我都唔知講D咩好")
        SVC_Article.addArticle("27052237", "測試標題dsagh", "測試一下啦， 内容要點寫，我都唔知講D咩好")
        SVC_Article.addArticle("27052245", "測試標題fgthui", "測試一下啦， 内容要點寫，我都唔知講D咩好")
        SVC_Article.addArticle("27152247", "測試tuiop", "測試一下啦， 内容要點寫，我都唔知啊，講D咩好")
        SVC_Article.addArticle("27052242", "測試標題1", "測試一下啦， 内容要點寫，我都唔知啊，講D咩好")
        SVC_Article.addArticle("27152247", "測試標題2", "測試一下啦， 内容要點寫，我都唔知啊，講D咩好")
        SVC_Article.addArticle("27052241", "測試標題dsagh", "測試一下啦， 内容要點寫，我都唔知啊，講D咩好")
        SVC_Article.addArticle("27052245", "測試標題fgthui", "測試一下啦， 内容要點寫，我都唔知啊，講D咩好")
        SVC_Article.addArticle("27052239", "測試tuiop", "測試一下啦， 内容要點寫，我都唔知啊，講D咩好")
    except Exception as e:
        print(e)
        traceback.print_exc()

def test_del():
    try:
        SVC_Article.delArticle("27052237", 5);
    except Exception as e:
        print(e)
        traceback.print_exc()

def test_get_by_id():
    try:
        print(SVC_Article.getArticleById(2))
    except Exception as e:
        print(e)
        traceback.print_exc()

def test_newest_hot():
    try:
        print(SVC_Article.getArticleNewestHot())
    except Exception as e:
        print(e)
        traceback.print_exc()

def test_getbyuid():
    try:
        print(SVC_Article.getArticleByUid("27052237"))
    except Exception as e:
        print(e)
        traceback.print_exc()


def test_get_newest():
    try:
        print(SVC_Article.getNewestArticles())
    except Exception as e:
        print(e)
        traceback.print_exc()


def main():
    # test_add()
    test_del()
    # test_get_by_id()
    # test_get_newest()
    # test_getbyuid()
    # test_newest_hot()


if __name__ == '__main__':
    main()