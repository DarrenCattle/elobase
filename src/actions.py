import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table, DateTime, func, MetaData
from sqlalchemy.orm import relationship, scoped_session, sessionmaker, query
from sqlalchemy import create_engine
from src.queries import Game, User

class Actions:

    engine = create_engine('sqlite:///alchemy.db')
    meta = MetaData(bind=engine)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    def players_table(name):
        return Table(name, Actions.meta,
                     Column('player_id', Integer, ForeignKey(User.id)),
                     Column('elo', Integer),
                     schema=None, extend_existing=True)

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
                     schema=None, extend_existing=True)

    def create_game_tables(name):
        player_tab = name.lower() + '_players'
        result_tab = name.lower() + '_results'

        players_table = Actions.players_table(player_tab)
        results_table = Actions.results_table(result_tab)

        players_table.create(bind=Actions.engine)
        results_table.create(bind=Actions.engine)
        print(player_tab + ' table created')
        print(result_tab + ' table created')

        new_game = Game(name=name)
        Actions.session.add(new_game)
        Actions.session.commit()
        print(name + ' game added to games table with id ' + str(new_game.id))

    def delete_game_tables(name):
        player_tab = name.lower() + '_players'
        result_tab = name.lower() + '_results'

        players_table = Actions.players_table(player_tab)
        results_table = Actions.results_table(result_tab)

        players_table.drop(Actions.engine)
        results_table.drop(Actions.engine)
        print(player_tab + ' table deleted')
        print(result_tab + ' table deleted')

        game = Actions.session.query(Game).filter(Game.name==name).first()
        if game is not None:
            Actions.session.delete(game)
            Actions.session.commit()
        print(name + ' game deleted from games table')


    def create_user(name, password):
        new_user = User(name=name, password=password)
        Actions.session.add(new_user)
        Actions.session.commit()
        print(name + ' user has been created with id ' + str(new_user.id))

    def delete_user(name):
        user = Actions.session.query(User).filter(User.name==name).first()
        if user is not None:
            Actions.session.delete(user)
            Actions.session.commit()
        print(name + ' user has been deleted')

    def authenticate_user(name, password):
        user = Actions.session.query(User).filter(User.name==name).first()
        if user.password == password:
            return True
        return False

    def name_available(name):
        user = Actions.session.query(User).filter(User.name==name).first()
        if user is None:
            return True
        return False

    def get_users():
        result = []
        users = Actions.session.query(User).all()
        for user in users:
            result.append(user.name)
        return result

    def get_games():
        result = []
        games = Actions.session.query(Game).all()
        for game in games:
            result.append(game.name)
        return result