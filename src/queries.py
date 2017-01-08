import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table, DateTime, func, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine('sqlite:///alchemy.db')
meta = MetaData(bind=engine)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def create_default():
    Base.metadata.create_all(engine)
    print('users and games created')

def create_game_tables(name):
    table_name = name.lower() + '_players'
    players_table = Table(table_name, meta,
                    Column('player_id', Integer, ForeignKey(User.id)),
                    Column('elo', Integer),
                    schema=None)

    table_name = name.lower() + '_results'
    results_table = Table(table_name, meta,
                    Column('id', Integer, primary_key=True),
                    Column('winner_id', Integer, ForeignKey(User.id)),
                    Column('winner_start_elo', Integer),
                    Column('winner_end_elo', Integer),
                    Column('loser_id', Integer, ForeignKey(User.id)),
                    Column('loser_start_elo', Integer),
                    Column('loser_end_elo', Integer),
                    Column('created', DateTime(timezone=True), default=func.now()),
                    schema=None)

    players_table.create(bind=engine)
    results_table.create(bind=engine)
    print(name + "_players and " + name + "_results have been created")

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