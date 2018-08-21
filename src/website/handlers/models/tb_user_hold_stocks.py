#coding=utf-8

from sqlalchemy import Column, Integer, DECIMAL, DateTime, String

from handlers.models.basemodel import BaseModel

from datetime import datetime

class UserStock(BaseModel):
    """
    用戶持倉的股票
    """

    __tablename__ = 'tb_user_hold_stocks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    u_id = Column(Integer, nullable=False)                          # 用戶id
    s_stock_code = Column(String(12), nullable=False)                  # 股票代碼
    s_stock_name = Column(String(16), nullable=False)                  # 股票名字
    s_stock_count = Column(Integer, default=0)                      # 持股數
    s_stock_price = Column(DECIMAL(15, 4), nullable=False)          # 持股成本價
    s_stock_freeze = Column(Integer, default=0)                   # 凍結的股數 A股T+1交易
    s_date          = Column(DateTime, default=datetime.now())      # 持股時間


    def __repr__(self):
        return  "TABLE <UserStock: %s>" % self.to_json()

    def to_json(self):
        return dict(
            uid = self.u_id,
            code = self.s_stock_code,
            name = self.s_stock_name,
            price = (float)(self.s_stock_price),
            count = self.s_stock_count,
            freeze = self.s_stock_freeze
        )

##################################################  TEST
from handlers.models.basemodel import Engin

def main():
    BaseModel.metadata.create_all(Engin)


if __name__ == '__main__':
    main()