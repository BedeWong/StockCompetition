#coding=utf-8

from sqlalchemy import Column, Integer, DateTime, String
from handlers.models.basemodel import BaseModel

from datetime import datetime

class Reply(BaseModel):
    """
    用中评论表，评论可以是：文章，用户发表的问题，股票新闻
    """

    __tablename__ = 'tb_reply'

    id = Column(Integer, primary_key=True, autoincrement=True)
    a_id = Column(Integer, nullable=False)
    u_id  = Column(Integer, nullable=False)
    r_reply_id = Column(Integer, default=0)
    r_time = Column(DateTime, default=datetime.now())
    r_content = Column(String(2048), default="")
    r_upcounts = Column(Integer, default=0)
    r_status = Column(Integer, default=0)

    def __repr__(self):
        return "TABLE <Reply: %s>" % self.to_json()

    def to_json(self):
        return dict(
            id = self.id,
            airticleid = self.a_id,
            uid = self.u_id,
            replyid = self.r_reply_id,
            pubtime = str(self.r_time),
            content = self.r_content,
            upcounts = self.r_upcounts
        )


from handlers.models.basemodel import Engin
def main():
    BaseModel.metadata.create_all(Engin)


if __name__ == '__main__':
    main()