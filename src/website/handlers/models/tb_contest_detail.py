#coding=utf-8

from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, Date, Float
from handlers.models.basemodel import BaseModel

from datetime import datetime

class ContestDetail(BaseModel):
    """
    比赛详情表：描述每场比赛的参赛人数，以及用户的当前战绩情况
    """
    __tablename__ = 'tb_contest_detail'

    id = Column(Integer, primary_key=True, autoincrement=True)
    c_id = Column(Integer, nullable= False)
    u_id = Column(Integer, nullable=False)
    c_money = Column(DECIMAL(15,4), default=0)
    c_mv = Column(DECIMAL(15, 4), default=0)
    c_win_rate = Column(Float, default=0.0)
    c_join_time = Column(DateTime, default=datetime.now())
    c_position = Column(Float, default=0)
    c_stock_count = Column(Integer, default=0)

    def __repr__(self):
        return "TABLE <ContestDetail: %s>" % self.to_json()

    def to_josn(self):
        return ""

def main():
    pass


if __name__ == '__main__':
    main()