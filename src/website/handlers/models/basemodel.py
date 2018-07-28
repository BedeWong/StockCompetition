#coding=utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker

import  config

Engin = create_engine(config.mysqlurl)
DBSession = sessionmaker(bind=Engin)
dbsession = DBSession()

BaseModel = declarative_base()
