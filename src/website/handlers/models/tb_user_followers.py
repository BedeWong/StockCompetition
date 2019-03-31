#coding=utf-8

from sqlalchemy import Column, String, Integer, DateTime
from handlers.models.basemodel import BaseModel, engine

class UserFollowers(BaseModel):
    """
    用户粉丝关系表, 一种单向关系，a是b的粉丝  不代表B也是A的分丝
    """

    __tablename__ = 'tb_followers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    u_id = Column(Integer, nullable=False)
    u_follower_id  = Column(Integer, nullable=False)

    def __repr__(self):
        return "TABLE <UserFollowers: %s>" % self.to_json()

    def to_json(self):
        return dict(
            uid  = self.u_id,
            fuid = self.u_follower_id
        )


from handlers.models.basemodel import Engin
def main():
    BaseModel.metadata.create_all(Engin)


if __name__ == '__main__':
    main()