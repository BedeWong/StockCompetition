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
    u_id = Column(Integer, nullable=False)          # 創建人
    c_create_time = Column(DateTime, default=datetime.now())
    c_title = Column(String(64), nullable=False)
    c_explain = Column(String(256), nullable=False)
    c_start_date = Column(Date, nullable=False)
    c_end_date = Column(Date, nullable=False)
    c_status = Column(Integer, default=0)       # 0未开始， 1进行中， 2结束，  3关闭    5 刪除
    c_default_capital = Column(DECIMAL(15, 4), default=500000)
    c_check_auth = Column(Integer, default=0)   # 0不需要申请认证   1需要申请认证
    c_logo_url = Column(String(64), default="images/logo6.jpg")

    def __repr__(self):
        return "TABLE <Contest: %s>" % self.to_json()

    def to_json(self):
        return dict(
            id = self.id,
            uid = self.u_id,
            createtime = (str)(self.c_create_time),
            title = self.c_title,
            desc = self.c_explain,
            stime = (str)(self.c_start_date),
            etime = (str)(self.c_end_date),
            status = self.c_status,
            money = (float)(self.c_default_capital),
            logo = self.c_logo_url
        )


#####   test
##
#
from handlers.models.basemodel import Engin
def main():
    BaseModel.metadata.create_all(Engin)


if __name__ == '__main__':
    main()