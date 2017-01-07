import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table, DateTime, func, MetaData
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///alchemy.db')
meta = MetaData(bind=engine)

def create_game_tables(name):
    table_name = name.lower() + '_players'
    players_table = Table(table_name, meta,
                          Column('player_id', Integer, ForeignKey('User.id')),
                          Column('elo', Integer),
                          schema=None)

    table_name = name.lower() + '_results'
    results_table = Table(table_name, meta,
                          Column('id', Integer, primary_key=True),
                          Column('winner_id', Integer, ForeignKey('User.id')),
                          Column('winner_start_elo', Integer),
                          Column('winner_end_elo', Integer),
                          Column('loser_id', Integer, ForeignKey('User.id')),
                          Column('loser_start_elo', Integer),
                          Column('loser_end_elo', Integer),
                          Column('created', DateTime(timezone=True), default=func.now()),
                          schema=None)

    players_table.create(bind=engine)
    results_table.create(bind=engine)