#coding=utf-8

from sqlalchemy import Column, String, Integer, DateTime
from handlers.models.basemodel import BaseModel

class UserMarks(BaseModel):
    """
    用户手藏表，收藏贴子，官方文章
    """
    __tablename__ = 'tb_marks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    u_id = Column(Integer, nullable=False)
    a_id = Column(Integer, nullable=False)
    m_type = Column(Integer, nullable=False)            # 1 官方文章   2 用户发表的文章

    def __repr__(self):
        return "TABLE <UserMarks: %s>" % self.to_json()

    def to_json(self):
        return ""

def main():
    pass


if __name__ == '__main__':
    main()