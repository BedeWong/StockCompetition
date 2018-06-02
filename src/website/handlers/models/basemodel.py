#coding=utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker

Engin = create_engine("mysql+mysqlconnector://wong:wong@120.79.208.53:3306/stockcontest?charset=utf8")
DBSession = sessionmaker(bind=Engin)
dbsession = DBSession()

BaseModel = declarative_base()
