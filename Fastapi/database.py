#first create the database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#database connection
#need to create database before to use this
DATABASE_URL = 'postgresql://postgres:harik1234@localhost/finance_db'

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()