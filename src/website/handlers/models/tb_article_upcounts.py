#coding=utf-8

from sqlalchemy import Column, Integer, DateTime, String
from handlers.models.basemodel import BaseModel

class ArticleUpcounts(BaseModel):
    """
    贴子点赞表，记录用户的点赞数据,不能重复点赞
    """

    __tablename__ = 'tb_article_upcounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    a_id = Column(Integer, nullable=False)
    u_id = Column(Integer, nullable=False)

    def __repr__(self):
        return "TABLE <ArticleUpcounts: %s>" % self.to_json()

    def to_josn(self):
        return ""

def main():
    pass


if __name__ == '__main__':
    main()