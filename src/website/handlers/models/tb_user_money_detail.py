#coding=utf-8

from sqlalchemy import Column, Integer, Date, DECIMAL
from handlers.models.basemodel import BaseModel

from datetime import  datetime

class UserMoneyDetail(BaseModel):
    """
    用户资产变动记录（日）
    每天一条记录，收盘后记录。
    """

    __tablename__ = 'tb_money_detail'

    id  = Column(Integer, primary_key=True, autoincrement=True)
    u_id = Column(Integer, nullable=False)
    m_date = Column(Date, default=datetime.now())
    m_money = Column(DECIMAL(15, 4), default=0)

    def __repr__(self):
        return "TABLE <UserMoneyDetail: %s>" % self.to_json()

    def to_josn(self):
        return ""

def main():
    pass


if __name__ == '__main__':
    main()