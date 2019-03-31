#coding=utf-8

from sqlalchemy import Column, Integer, DateTime, String
from handlers.models.basemodel import BaseModel

from datetime import datetime

class Article(BaseModel):
    """
    文章表，用户发表
    """
    __tablename__ = 'tb_article'

    id = Column(Integer, primary_key=True, autoincrement=True)
    u_id = Column(Integer, nullable=False)
    a_title = Column(String(128), nullable=False)
    a_content = Column(String(4096), nullable=False)
    a_pub_time = Column(DateTime, default=datetime.now())
    a_modify_time = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    a_status = Column(Integer, default=0)         # 贴子状态：  0 审核中
                                                  #        1 通过审核  2 关闭(刪除)
    a_upcounts = Column(Integer, default=0)
    a_interviews = Column(Integer, default=0)
    a_replys = Column(Integer, default=0)

    def __repr__(self):
        return "TABLE <Airticle: %s>" % self.to_json()

    def to_json(self):
        return dict(
            id = self.id,
            uid = self.u_id,
            title = self.a_title,
            content = self.a_content,
            pubtime = str(self.a_pub_time),
            upcounts = self.a_upcounts,
            interviews = self.a_interviews,
            replays = self.a_replys
        )

from handlers.models.basemodel import Engin
def main():
    BaseModel.metadata.create_all(Engin)


if __name__ == '__main__':
    main()