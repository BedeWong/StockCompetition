#coding=utf-8

from sqlalchemy import Column, Integer, String
from handlers.models.basemodel import BaseModel

from datetime import datetime

class ContestUserStocks(BaseModel):
    """
    比赛用户持股数
    """

    __tablename__ = 'tb_contest_user_stocks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    c_id =  Column(Integer, nullable=False)
    u_id = Column(Integer, nullable=False)
    s_id = Column(Integer, nullable=False)
    s_code = Column(String(8), nullable=False)
    s_stock_count = Column(Integer, default=0)

    def __repr__(self):
        return "TABLE <ContestUserStocks: %s>" % self.to_json()

    def to_josn(self):
        return ""

def main():
    pass


if __name__ == '__main__':
    main()