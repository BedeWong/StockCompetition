#coding=utf-8

from handlers.models.basemodel import BaseModel, Engin

def main():
    """
    创建数据库表，
    所有被创建的表都继承自BaseModel
    :return:

    ###!!!! 失效
    """

    BaseModel.metadata.create_all(Engin)


if __name__ == '__main__':
    main()