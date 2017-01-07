import os
import sqlite3
import sqlalchemy
from sqlalchemy import create_engine

class Database:

    engine = create_engine('sqlite:///:memory:', echo=True)
    conn = sqlite3.connect('elobase.db',check_same_thread=False)
    print("Opened elobase successfully")

    @staticmethod
    def createPlayerMaster():
        data = '''CREATE TABLE player_master (
        id INT PRIMARY KEY NOT NULL,
        name TEXT NOT NULL,
        password TEXT
        );'''
        Database.conn.execute(data)
        print("table player_master(id, name, password) created")

    @staticmethod
    def createGameMaster():
        data = '''CREATE TABLE game_master (
        id INT PRIMARY KEY NOT NULL,
        name TEXT NOT NULL
        );'''
        Database.conn.execute(data)
        print("table game_master(id, name) created")

    @staticmethod
    def createGameTable(game_name):

        name = game_name.lower()

        #create game_players table
        player_table = 'CREATE TABLE ' + name + '''_players(
        player_id INT NOT NULL REFERENCES player_master(id),
        elo INT NOT NULL
        );'''
        Database.conn.execute(player_table)
        print("table " + name + "_players(player_id, elo) created")

        #create game_results table
        result_table = 'CREATE TABLE ' + name + '''_results(
        id INT PRIMARY KEY NOT NULL,
        winner_id INT NOT NULL REFERENCES player_master(id),
        winner_original_elo INT NOT NULL,
        winner_result_elo INT NOT NULL,
        loser_id INT NOT NULL REFERENCES player_master(id),
        loser_original_elo INT NOT NULL,
        loser_result_elo INT NOT NULL,
        created DATETIME NOT NULL
        );'''
        Database.conn.execute(result_table)
        print("table " + name + "_results(alot) created")

        #insert into game_master table
        fresh_id = Database.getFreshID("game_master")
        builder = "VALUES (" + fresh_id + ",'" + name + "')"
        query_string = "INSERT INTO game_master (ID,NAME) " + builder
        Database.conn.execute(query_string)

        Database.conn.commit()
        print(query_string)
        print(name + " inserted into game table with " + fresh_id)


    @staticmethod
    def getFreshID(table):
        query_string = "SELECT id from " + table
        result = Database.conn.execute(query_string)
        id_list = []
        for row in result:
            id_list.append(row[0])
        for x in range(1,len(id_list)+2):
            if x not in id_list:
                return str(x)

    @staticmethod
    def createPlayer(player, pwd):
        builder = "VALUES (" + player.id + ",'" + player.name + "','" + pwd + "')"
        query_string = "INSERT INTO player_master (ID,NAME,PASSWORD) " + builder
        Database.conn.execute(query_string)
        Database.conn.commit()
        print(query_string)
        print(player.name + " inserted into player_master table with " + player.id)

    @staticmethod
    def createResult(game_id, winner_id, winner_elo, winner_result, loser_id, loser_elo, loser_result):
        game_name = Database.getGameName(game_id)
        table_name = game_name + "_results"
        fresh_id = Database.getFreshID(table_name)
        builder = "VALUES (" + str(fresh_id) + "," + str(winner_id) + "," + str(winner_elo) + "," + str(winner_result)
        builder += "," + str(loser_id) + "," + str(loser_elo) + "," + str(loser_result) + ",DATETIME('now') )"
        query_string = "INSERT INTO " + table_name + " (ID,WINNER_ID,WINNER_ORIGINAL_ELO,WINNER_RESULT_ELO,LOSER_ID,LOSER_ORIGINAL_ELO,LOSER_RESULT_ELO,CREATED) " + builder
        Database.conn.execute(query_string)
        Database.conn.commit()
        Database.createEntry(game_id, winner_id, winner_result)
        Database.createEntry(game_id, loser_id, loser_result)
        print(str(Database.getPlayerName(winner_id)) + " inserted into result table with " + str(winner_elo))

    @staticmethod
    def createEntry(game_id, player_id, player_elo):
        game_name = Database.getGameName(game_id)
        table_name = game_name + "_players"
        query_string = "UPDATE " + table_name + " set ELO = " + str(player_elo) + " where PLAYER_ID=" + str(player_id)
        if(Database.getElo(player_id, game_id) == 1000):
            query_string = "INSERT INTO " + table_name + " (PLAYER_ID,ELO) VALUES ( + " + str(player_id) + "," + str(player_elo) + ")"
        Database.conn.execute(query_string)
        Database.conn.commit()

    @staticmethod
    def getPlayerName(player_id):
        header = "SELECT id, name from player_master WHERE id='" + str(player_id) + "'"
        result = Database.conn.execute(header)
        for row in result:
            #print("PLAYER_ID = " + str(row[0]))
            #print("PLAYER_NAME = " + str(row[1]))
            return row[1]
        return 0

    @staticmethod
    def getGameTable():
        header = "SELECT id, name from game_master"
        result = Database.conn.execute(header)
        builder = ""
        for row in result:
            builder += '<li>' + 'ID: ' + str(row[0]) + ' NAME: ' + str(row[1]) + '</li>'
        return builder

    @staticmethod
    def getPlayerTable():
        header = "SELECT id, name from player_master"
        result = Database.conn.execute(header)
        builder = ""
        for row in result:
            builder += '<li>' + 'ID: ' + str(row[0]) + ' NAME: ' + str(row[1]) + '</li>'
        return builder

    @staticmethod
    def getGameName(game_id):
        header = "SELECT id, name from game_master WHERE id='" + str(game_id) + "'"
        result = Database.conn.execute(header)
        for row in result:
            #print("GAME_ID = " + str(row[0]))
            #print("GAME_NAME = " + str(row[1]))
            return row[1]

    @staticmethod
    def authenticatePlayer(username, password):
        header = "SELECT id, name, password from player_master WHERE name='" + username + "'"
        result = Database.conn.execute(header)
        for row in result:
            if(password == str(row[2])):
                return True
        return False

    @staticmethod
    def nameAvailable(name):
        header = "SELECT id, name, password from player_master WHERE name='" + str(name) + "'"
        cursor = Database.conn.execute(header)
        for row in cursor:
            return False
        return True

    @staticmethod
    def getElo(player_id,game_id):
        header = "SELECT player_id, elo from " + Database.getGameName(game_id) + "_players WHERE player_id='" + str(player_id) + "'"
        result = Database.conn.execute(header)
        count = 0
        elo = 1000
        for row in result:
            count += 1
            elo = row[1]
        if count == 0:
            print("no results found, therefore ELO is default 1000")
            return elo
        #print(str(player_id) + " player elo: " + str(elo))
        return elo

