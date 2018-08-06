#coding=utf-8

from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, Date
from handlers.models.basemodel import BaseModel

from datetime import datetime

class Contest(BaseModel):
    """
    比赛信息表
    """

    __tablename__ = 'tb_contest'

    id = Column(Integer, primary_key=True, autoincrement=True)
    u_id = Column(Integer, nullable=False)
    c_create_time = Column(DateTime, default=datetime.now())
    c_title = Column(String(64), nullable=False)
    c_explain = Column(String(256), nullable=False)
    c_start_date = Column(Date, nullable=False)
    c_end_date = Column(Date, nullable=False)
    c_status = Column(Integer, default=0)       # 0未开始， 1进行中， 2结束，  3关闭
    c_default_capital = Column(DECIMAL(15, 4), default=500000)
    c_check_auth = Column(Integer, default=0)   # 0不需要申请认证   1需要申请认证
    c_logo_url = Column(String(64), default="")

    def __repr__(self):
        return "TABLE <Contest: %s>" % self.to_json()

    def to_josn(self):
        return ""

def main():
    pass


if __name__ == '__main__':
    main()