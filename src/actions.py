import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table, DateTime, func, MetaData
from sqlalchemy.orm import relationship, scoped_session, sessionmaker, mapper
from sqlalchemy import create_engine
from database import Database
from queries import Game, User

class Actions:

    engine = create_engine('sqlite:///alchemy.db')
    meta = MetaData(bind=engine)

    def players_table(name):
        return Table(name, Actions.meta,
                     Column('player_id', Integer, ForeignKey(User.id)),
                     Column('elo', Integer),
                     schema=None)

    def results_table(name):
        return Table(name, Actions.meta,
                     Column('id', Integer, primary_key=True),
                     Column('winner_id', Integer, ForeignKey(User.id)),
                     Column('winner_start_elo', Integer),
                     Column('winner_end_elo', Integer),
                     Column('loser_id', Integer, ForeignKey(User.id)),
                     Column('loser_start_elo', Integer),
                     Column('loser_end_elo', Integer),
                     Column('created', DateTime(timezone=True), default=func.now()),
                     schema=None)

    def create_game_tables(self,name):
        player_tab = name.lower() + '_players'
        result_tab = name.lower() + '_results'

        players_table = Actions.players_table(player_tab)
        results_table = Actions.results_table(result_tab)

        players_table.create(bind=Actions.engine)
        results_table.create(bind=Actions.engine)

    def delete_game_tables(self,name):
        table_players = name.lower() + '_players'
        table_results = name.lower() + '_results'
        Game.query.filter_by(name=name).delete()
        Database.deleteTable(table_players)
        Database.deleteTable(table_results)

    def delete_game_tables1(self,name):
        player_tab = name.lower() + '_players'
        result_tab = name.lower() + '_results'

        players_table = Actions.players_table(player_tab)
        results_table = Actions.results_table(result_tab)

        players_table.drop(Actions.engine)
        results_table.drop(Actions.engine)
        #Game.query.filter_by(name=name).delete()
        print(player_tab + ' table created')
        print(result_tab + ' table created')


