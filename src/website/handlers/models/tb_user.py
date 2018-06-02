#coding=utf-8

from sqlalchemy import Column, String, Integer, DECIMAL, DateTime, TIMESTAMP

import datetime
import json

from handlers.models.basemodel import BaseModel, Engin

class User(BaseModel):
    """用户表"""
    __tablename__ = 'tb_user'

    id              = Column(Integer, primary_key=True, autoincrement=True)
    u_name          = Column(String(20), unique=True, nullable=False)
    u_address       = Column(String(32), default='广州')
    u_mobilephone   = Column(String(16), unique=True, nullable=False)
    u_sex           = Column(Integer, default=0)
    u_vistors       = Column(Integer, default=0)
    u_passwd        = Column(String(32), nullable=False)
    u_paypwd        = Column(String(32), default='123456')
    u_headurl       = Column(String(32), default='')
    u_describe      = Column(String(256), default='')
    u_descimg       = Column(String(32), default='')
    u_level         = Column(Integer, default=1) # 1级，愣头青
    u_type          = Column(Integer, default=1) # 1 个人号，2平台号，3机构号
    u_earn_rate     = Column(DECIMAL(8, 2), default=0.0)
    u_earn_rate_mon = Column(DECIMAL(8, 2), default=0.0)
    u_win_rate      = Column(DECIMAL(8, 2), default=0.0)
    u_money         = Column(DECIMAL(36, 4), default=5000000.0)
    u_status        = Column(Integer, default=0)
    u_regtime       = Column(DateTime, default=datetime.datetime.now())
    u_lastlogin     = Column(DateTime, default=datetime.datetime.now())
    u_recom_id      = Column(Integer, default=0)  # 平台推挤
    u_email         = Column(String(32), default='')
    u_rank          = Column(Integer, default=0) # 未排名


    def __repr__(self):
        return "<User: %s>" % self.to_json();

    def to_dict(self):
        return dict(
            uid = self.id,
            uname = self.u_name,
            uaddress = self.u_address,
            umobile = self.u_mobilephone,
            usex = self.u_sex,
            uvisitors = self.u_vistors,
            uheadurl = self.u_headurl,
            udescibe = self.u_describe,
            udescimg = self.u_descimg,
            ulevel = self.u_level,
            utype = self.u_type,
            uearnrate = (float)(self.u_earn_rate),
            uearnratemon = (float)(self.u_earn_rate_mon),
            uwinrate = (float)(self.u_win_rate),
            umoney = (float)(self.u_money),
            ulastlogin = (str)(self.u_lastlogin),
            uemail = self.u_email,
            urank = self.u_rank
        )

    def to_json(self):
        return json.dumps( dict(
            uid = self.id,
            uname = self.u_name,
            uaddress = self.u_address,
            umobile = self.u_mobilephone,
            usex = self.u_sex,
            uvisitors = self.u_vistors,
            uheadurl = self.u_headurl,
            udescibe = self.u_describe,
            udescimg = self.u_descimg,
            ulevel = self.u_level,
            utype = self.u_type,
            uearnrate = (float)(self.u_earn_rate),
            uearnratemon = (float)(self.u_earn_rate_mon),
            uwinrate = (float)(self.u_win_rate),
            umoney = (float)(self.u_money),
            ulastlogin = (str)(self.u_lastlogin),
            uemail = self.u_email,
            urank = self.u_rank
        ) )


####  test
from faker import Faker
from sqlalchemy.orm import sessionmaker
from handlers.models.basemodel import Engin

import hashlib

DBSession = sessionmaker(bind=Engin)
def insert_test_data():
    session = DBSession()

    md5obj = hashlib.md5()
    md5obj.update(b"123456")
    pwd = md5obj.hexdigest()

    fk = Faker(locale='zh-cn')
    session.execute(
        User.__table__.insert(), [
            {
                "u_name"    : fk.name(),
                "u_address"      : fk.province(),
                "u_mobilephone"  : fk.phone_number(),
                "u_sex"            : fk.random_int(0,1),
                "u_email"           : fk.email(),
                "u_passwd"          : pwd
            }
         for i in range(100)
        ]
    )
    session.commit()
    session.close()

def main():
    BaseModel.metadata.create_all(Engin)


def test_setattr():
    fk = Faker(locale='zh-cn')

    md5obj = hashlib.md5()
    md5obj.update(b"123456")
    pwd = md5obj.hexdigest()

    userobj = {
                "u_name"    : fk.name(),
                "u_address"      : fk.province(),
                "u_mobilephone"  : fk.phone_number(),
                "u_sex"            : fk.random_int(0,1),
                "u_email"           : fk.email(),
                "u_passwd"          : pwd
            }

    session = DBSession()
    user = session.query(User).filter_by(id=27052237).one()
    for k, v in userobj.items():
        if v is not None:
            setattr(user, k, v)

    print(user)

    session.merge(user)
    session.commit()
    session.close()

def test_toJSON():
    session = DBSession()
    user = session.query(User).get(27052237)
    print(user.to_json())

if __name__ == '__main__':
    test_toJSON()