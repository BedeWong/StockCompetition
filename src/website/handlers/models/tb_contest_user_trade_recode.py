#coding=utf-8

from sqlalchemy import Column, Integer, DECIMAL, DateTime, String

from handlers.models.basemodel import BaseModel

from datetime import datetime

class TradeRecode(BaseModel):
    """
    用戶的交易歷史記錄，用戶提交請求，先請求交易系統委托下單（撤銷），待交易系統返回數據成功則添加紀錄
    保存交易記錄
    """

    __tablename__ = 'tb_contest_user_stock_recode'

    id = Column(Integer, primary_key=True, autoincrement=True)
    u_id = Column(Integer, nullable=False)
    s_id = Column(String(12), nullable=False)  # 股票ID
    s_code = Column(String(12), nullable=False) # 股票代碼 如：sh603036
    s_name = Column(String(16), nullable=False)  # 股票名字
    t_type = Column(Integer, nullable=False)   # 交易類型   1買入、2賣出
    t_status = Column(Integer, nullable=False, default=0)    # 當前狀態：0交易進行中   1交易完成  2 撤單
    t_submit_time   = Column(DateTime, default=datetime.now())  # 委托時間
    t_finish_time = Column(DateTime)  # 完成時間
    t_charge  = Column(DECIMAL(12, 2), nullable=False) # 手續費
    t_stock_price = Column(DECIMAL(12, 2), nullable=False)    # 委托價
    t_volume       = Column(DECIMAL(15, 2), nullable=False)    # 成交額
    t_stock_amount = Column(Integer, nullable=False)    # 買入、賣出 股數

    c_id   = Column(Integer, nullable=False)            #  比賽id

    def __repr__(self):
        return "TABLE <TradeRecode: %s>" % self.to_json()

    def to_json(self):
        return dict(
            id = self.id,     # 撤單需要此id
            uid = self.u_id,
            code = self.s_code,
            name = self.s_name,
            type = self.t_type,
            status = self.t_status,
            submit_time = (str)(self.t_submit_time),
            finish_time = (str)(self.t_finish_time),
            charge = (float)(self.t_charge),
            price = (float)(self.t_stock_price),
            amount = self.t_stock_amount,
            volume = (float)(self.t_volume),
            cid  =  self.c_id
        )


##################################################  TEST
from handlers.models.basemodel import Engin

def main():
    BaseModel.metadata.create_all(Engin)



if __name__ == '__main__':
    main()