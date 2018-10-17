#coding=utf-8

from sqlalchemy import Column, String, Integer, DateTime
from handlers.models.basemodel import BaseModel

from datetime import  datetime

class Dongtaitype(object):
    follower = 1                ## 關注
    reply = 2                   ## 回復
    upcount_topic = 3                 ##  點贊 話題
    upcount_reply = 4               ## 點贊回復
    pub_topic = 5               # 發表話題
    pub_reply = 6               # 發表回復
    buy_sale_stock = 7          # 買賣股票
    invoke_stock = 8            # 撤單
    mark_article = 9               # 收藏文章

class UserDongtai(BaseModel):
    """
    用户动态model，获取用户的动态
    """
    __tablename__ = 'tb_user_dongtai'

    id = Column(Integer, primary_key=True, autoincrement=True)
    d_type = Column(Integer, nullable=False)            #  动态类型：1关注  2回复  3点赞  4发表贴子  5发表回复  6下单  7撤单  8收藏（文章、贴子）
    u_id = Column(Integer, nullable=False, index=True)  # 用户id， 这个id标识谁收到这条消息
    u_refuid = Column(Integer, nullable=False)          # 用户id，标识谁关注我/评论我/点赞我。。。
    d_time = Column(DateTime, default=datetime.now())   # 用户触发时间，u_refuid 在 这个时间 对 u_id 了 d_type的事情
    d_extmsg = Column(String(256), default="")          # 附加消息，用于展示
    d_refaid = Column(Integer, default=0)               # 主题id，可以是贴子id，用户id，新闻id。。

    def __repr__(self):
        return "TABLE <UserDongtai: %s>" % self.to_json()


    def to_json(self):
        return dict(
            id = self.id,
            type = self.d_type,
            uid = self.u_id,
            fuid = self.u_refuid,
            time = (str)(self.d_time),
            extmsg = self.d_extmsg,
            aid = self.d_refaid
        )


from handlers.models.basemodel import Engin
def main():
    BaseModel.metadata.create_all(Engin)


if __name__ == '__main__':
    main()