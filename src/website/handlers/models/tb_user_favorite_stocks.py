#coding=utf-8

from sqlalchemy import Column, Integer, String
from handlers.models.basemodel import BaseModel

class UserFavoriteStocks(BaseModel):
    """
    用户收藏的股票，自选股列表
    """
    __tablename__ = 'tb_favorite_stocks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    u_id = Column(Integer, nullable=False)
    s_stock_id = Column(Integer, nullable=False, default=0)
    s_stock_code = Column(String(12), default='')
    s_stock_name = Column(String(16), default="")

    def __repr__(self):
        return "TABLE <UserFavoriteStocks: %s>" % self.to_json()

    def to_json(self):
        return dict(
            uid = self.u_id,
            code = self.s_stock_code,
            name = self.s_stock_name,
            sid = self.s_stock_id
        )


from handlers.models.basemodel import Engin
def main():
    BaseModel.metadata.create_all(Engin)


if __name__ == '__main__':
    main()