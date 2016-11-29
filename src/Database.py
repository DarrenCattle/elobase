import os
import sqlite3

class Database:

    conn = sqlite3.connect('elobase.db')
    games = []
    print("Opened elobase successfully")

    def createGame(self, name):
        query_string = "CREATE TABLE " + name + '''(ID INT PRIMARY KEY     NOT NULL,
        NAME           TEXT    NOT NULL,
        SUMMARY        TEXT    NOT NULL,
        RATING         TEXT    NOT NULL);'''
        Database.conn.execute(query_string)
        print(name + " empty table created successfully")

    def createMaster(self, name):
        query_string = "CREATE TABLE MASTER " + '''(ID INT PRIMARY KEY     NOT NULL,
        NAME           TEXT    NOT NULL,
        DATA           TEXT    NOT NULL,
        RECORD         TEXT    NOT NULL,
        GAMES          INT     NOT NULL,
        RATING         INT     NOT NULL);'''
        Database.conn.execute(query_string)
        print(name + " empty table created successfully")

    @staticmethod
    def getFreshID():
        query_string = "SELECT id, name, data, record, games, rating  from " + game
        result = Database.conn.execute(query_string)
        id_list = []
        for row in result:
            id_list.append(row[0])
        for x in range(1,len(id_list)+2):
            if x not in id_list:
                return str(x)

    @staticmethod
    def createPlayer(player):
        builder = "VALUES (" + createID(game) + ",'" + player.name + "','fill','fill',1," + str(player.elo) + ")"
        query_string = "INSERT INTO " + game + " (ID,NAME,DATA,RECORD,GAMES,RATING) " + builder
        Database.conn.execute(query_string)
        Database.conn.commit()
        print(query_string)
        print(player.name + " inserted into " + game)

    def insertPlayer(game, player):

        builder = "VALUES (" + createID(game) + ",'" + player.name + "','fill','fill',1," + str(player.elo) + ")"
        query_string = "INSERT INTO " + game + " (ID,NAME,DATA,RECORD,GAMES,RATING) " + builder
        Database.conn.execute(query_string)
        Database.conn.commit()
        print(query_string)
        print(player.name + " inserted into " + game)

    def updateRating(game, player):
        query_string = "UPDATE " + game + " set RATING = "+str(player.elo)+" where NAME='" + player.name + "'"
        Database.conn.execute(query_string)
        Database.conn.commit()
        print(query_string)
        print(player.name + " updated in " + game)

    def getGame(self, game):
        header = "SELECT id, name, data, record, games, rating  from " + game
        result = Database.conn.execute(header)
        for row in result:
            print("ID = " + str(row[0]))
            print("NAME = " + str(row[1]))
            print("GAMES = " + str(row[4]))
            print("RATING = " + str(row[5]))

    def getPlayer(self, game, player):
        header = "SELECT id, name, data, record, games, rating  from " + game + " WHERE NAME='" + player.name + "'"
        result = Database.conn.execute(header)
        for row in result:
            print("ID = " + str(row[0]))
            print("NAME = " + str(row[1]))
            print("GAMES = " + str(row[4]))
            print("RATING = " + str(row[5]))