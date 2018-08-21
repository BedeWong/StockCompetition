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
    c_rank  = Column(Integer, default=0)
    c_status  = Column(Integer, default=0)   # 用戶狀態：0正常，1 已退出

    def __repr__(self):
        return "TABLE <ContestDetail: %s>" % self.to_json()

    def to_json(self):
        return dict(
            contestid = self.c_id,
            uid = self.u_id,
            money =  (float)(self.c_money),
            marketvalue = (float)(self.c_mv),
            winrate = self.c_win_rate,
            jointime = (str)(self.c_join_time),
            position = self.c_position,
            rank   = self.c_rank,
            status = self.c_status
        )

##############  test
###
from handlers.models.basemodel import Engin
def main():
    BaseModel.metadata.create_all(Engin)


if __name__ == '__main__':
    main()