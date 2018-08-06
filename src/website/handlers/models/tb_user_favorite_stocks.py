#coding=utf-8

from sqlalchemy import Column, Integer
from handlers.models.basemodel import BaseModel

class UserFavoriteStocks(BaseModel):
    """
    用户收藏的股票，自选股列表
    """
    __tablename__ = 'tb_favorite_stocks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    u_id = Column(Integer, nullable=False)
    s_stock_id = Column(Integer, nullable=False)

    def __repr__(self):
        return "TABLE <UserFavoriteStocks: %s>" % self.to_json()

    def to_josn(self):
        return ""

def main():
    pass


if __name__ == '__main__':
    main()