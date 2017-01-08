import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table, DateTime, func, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker, query
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine('sqlite:///alchemy.db')
meta = MetaData(bind=engine)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def create_default():
    Base.metadata.create_all(engine)
    print('users and games created')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    password = Column(String)

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Game %r>' % (self.name)

class Elo(Base):
    name = ""
    __tablename__ = name + '_results'
    id = Column(Integer, primary_key=True)
    elo = Column(Integer)

    def __init__(self, id=None, elo=None):
        self.id = id
        self.elo = elo

    def __repr__(self):
        return '<Elo %r>' % (self.elo)