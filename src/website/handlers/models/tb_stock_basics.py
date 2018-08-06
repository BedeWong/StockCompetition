#coding=utf-8

from sqlalchemy import Column, Integer, String, Float, BigInteger
from handlers.models.basemodel import BaseModel

class StockBaiscs(BaseModel):
    """
    A股基本数据
    """

    __tablename__ = 'tb_stock_basics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(8))
    name = Column(String(16))
    industry = Column(String(16))
    area = Column(String(16))
    pe = Column(Float)
    outstanding = Column(Float)
    totals = Column(Float)
    totalAssets = Column(Float)
    liquidAssets = Column(Float)
    fixedAssets = Column(Float)
    reserved = Column(Float)
    reservedPerShare = Column(Float)
    esp = Column(Float)
    bvps = Column(Float)
    pb = Column(Float)
    timeToMarket = Column(BigInteger(20))
    undp = Column(Float)
    perundp = Column(Float)
    rev = Column(Float)
    profit = Column(Float)
    gpr = Column(Float)
    npr = Column(Float)
    holders = Column(Float)

    def __repr__(self):
        return "TABLE <StockBaiscs: %s>" % self.to_json()

    def to_josn(self):
        return ""


def main():
    pass


if __name__ == '__main__':
    main()