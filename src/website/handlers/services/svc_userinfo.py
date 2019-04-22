#coding=utf-8

from handlers.models.tb_user import User
from handlers.models.basemodel import dbsession

import logging

class SVC_userinfo(object):
    '''
    用户表相关服务
    '''

    @staticmethod
    def add_user(**kwargs):
        user = User()
        user.u_name = kwargs.get('u_name')
        user.u_passwd = kwargs.get('u_pwd')
        user.u_email = kwargs.get('u_email')
        user.u_sex = kwargs.get('u_sex')
        logging.debug('SVC_userinfo 注册用户：', user)

        dbsession.add(user)
        dbsession.commit()

        return user

    @staticmethod
    def delete_user(arg):

        user =  None
        try:
            if isinstance(arg, int):
                user = dbsession.query(User).filter_by(id=arg).one()

            if user is not None:
                dbsession.delete(user)
                dbsession.commit()
            else:
                logging.error("delete_user:user obj is not a User instance.")
        except Exception as e:
            logging.error(e)
            dbsession.rollback()
            raise e

    @staticmethod
    def update_user(user=None, **kwargs):
        """

        :param kwargs:
        :return:
        """

        user_obj = {}

        if isinstance(user, User):
            user_obj = user
            logging.debug("user is User instance.")
            print("user is User instance.")

        else:
                if 'id' in kwargs:
                    user_obj = dbsession.query(User).filter_by(id=kwargs['id']).one()

        for k, v in kwargs.items():
            if k == 'id':
                continue

            if v is not None:
                setattr(user_obj, k, v)
        try:
            logging.debug(user_obj)
            print(user_obj)

            dbsession.merge(user_obj)
            dbsession.commit()
        except Exception as e:
            logging.error(e)
            dbsession.rollback()
            raise e

    @staticmethod
    def get_user_byid(id):
        """

        :param id:  用户id
        :return: 用户对象
        """
        user = None
        try:
            user = dbsession.query(User).get(id)
        except Exception as e:
            logging.error(e)
            dbsession.rollback()
            raise e
        return user

    @staticmethod
    def get_user_byname(name):

        if not isinstance(name, str):
            raise TypeError("name 类型错误", name)

        try:
            user = dbsession.query(User).filter_by(u_name=name).one()
        except Exception as e:
            logging.error(e)
            dbsession.rollback()
            raise e
        return user

    @staticmethod
    def get_user_byemail(email):
        if not isinstance(email, str):
            raise TypeError("name 类型错误", email)

        try:
            user = dbsession.query(User).filter_by(u_email=email).one()
        except Exception as e:
            logging.error(e)
            dbsession.rollback()
            raise e
        return user

    @staticmethod
    def get_user_bymobile(mobile):
        if not isinstance(mobile, str):
            raise TypeError("name 类型错误", mobile)
        try:
            user = dbsession.query(User).filter_by(u_mobilephone=mobile).one()
        except Exception as e:
            logging.error(e)
            dbsession.rollback()
            raise e
        return user

#### test
def test():
    # SVC_userinfo.update_user(id=27052237, u_name="wong")

    import hashlib
    md5obj = hashlib.md5()
    md5obj.update(b"123456")
    pwd = md5obj.hexdigest()
    SVC_userinfo.add_user(User(u_name="Bide", u_address="湖南", u_email='1005679098@qq.com', u_sex=1, u_mobilephone=10000000000, u_passwd=pwd))

def test_delete():
    SVC_userinfo.delete_user(27152548)

def test_update():
    user = SVC_userinfo.get_user_byid(27052238)
    if user is not None:
        SVC_userinfo.update_user(user, u_name="老王", u_vistors=80)

def test_query():
    user =  SVC_userinfo.get_user_byname("BideWong")
    if user is not None:
        print(user.to_json())

def main():
    test_query()
    test_query()


if __name__ == '__main__':
    main()