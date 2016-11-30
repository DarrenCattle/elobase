import os
import sqlite3

class Database:

    conn = sqlite3.connect('elobase.db',detect_types=sqlite3.PARSE_DECLTYPES)
    print("Opened elobase successfully")

    @staticmethod
    def createMaster():
        data = '''CREATE TABLE player (
        id INT PRIMARY KEY NOT NULL,
        name TEXT NOT NULL
        );

        CREATE TABLE game (
        id INT PRIMARY KEY NOT NULL,
        name TEXT NOT NULL
        );

        CREATE TABLE instance (
        id INT PRIMARY KEY NOT NULL,
        created DATETIME NOT NULL,
        game_id INT NOT NULL REFERENCES game(id),
        winner_id INT NOT NULL REFERENCES player(id),
        loser_id INT NOT NULL REFERENCES player(id)
        );

        CREATE TABLE result (
        id INT PRIMARY KEY NOT NULL,
        created DATETIME NOT NULL,
        game_id INT NOT NULL REFERENCES game(id),
        instance_id INT NOT NULL REFERENCES instance(id),
        player_id INT NOT NULL REFERENCES player(id),
        elo INT NOT NULL
        );'''
        queries = data.split(";")
        for query in queries:
            Database.conn.execute(query)
        print("master 4 tables created")

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
    def createPlayer(player):
        builder = "VALUES (" + player.id + ",'" + player.name + "')"
        query_string = "INSERT INTO player (ID,NAME) " + builder
        Database.conn.execute(query_string)
        Database.conn.commit()
        print(query_string)
        print(player.name + " inserted into player table with " + player.id)

    @staticmethod
    def createGame(name):
        fresh_id = Database.getFreshID("game")
        builder = "VALUES (" + fresh_id + ",'" + name + "')"
        query_string = "INSERT INTO game (ID,NAME) " + builder
        Database.conn.execute(query_string)
        Database.conn.commit()
        print(query_string)
        print(name + " inserted into game table with " + fresh_id)

    @staticmethod
    def createInstance(winner_id, loser_id, game_id):
        fresh_id = Database.getFreshID("instance")
        builder = "VALUES (" + fresh_id + "," + str(game_id) + "," + str(winner_id) + "," + str(loser_id) + ",DATETIME('now'))"
        query_string = "INSERT INTO instance (ID,GAME_ID,WINNER_ID,LOSER_ID,CREATED) " + builder
        Database.conn.execute(query_string)
        Database.conn.commit()
        #print(query_string)
        print(str(winner_id) + " inserted into instance table with ID " + str(fresh_id))
        return fresh_id

    @staticmethod
    def createResult(game_id, instance_id, player_id, elo):
        fresh_id = Database.getFreshID("result")
        builder = "VALUES (" + fresh_id + ",DATETIME('now')," + str(game_id) + "," + str(instance_id) + "," + str(player_id) + "," + str(elo) + ")"
        query_string = "INSERT INTO result (ID,CREATED,GAME_ID,INSTANCE_ID,PLAYER_ID,ELO) " + builder
        Database.conn.execute(query_string)
        Database.conn.commit()
        #print(query_string)
        print(str(Database.getPlayerName(player_id)) + " inserted into result table with " + str(Database.getElo(player_id,game_id)))

    @staticmethod
    def getPlayerName(player_id):
        header = "SELECT id, name from player WHERE id='" + str(player_id) + "'"
        result = Database.conn.execute(header)
        for row in result:
            #print("PLAYER_ID = " + str(row[0]))
            #print("PLAYER_NAME = " + str(row[1]))
            return row[1]
        return 0

    @staticmethod
    def getGameName(game_id):
        header = "SELECT id, name from game WHERE id='" + str(game_id) + "'"
        result = Database.conn.execute(header)
        for row in result:
            #print("GAME_ID = " + str(row[0]))
            #print("GAME_NAME = " + str(row[1]))
            return row[1]

    @staticmethod
    def getElo(player_id,game_id):
        header = "SELECT id, created, game_id, player_id, elo from result WHERE player_id='" + str(player_id) + "' AND game_id='" + str(game_id) + "'"
        result = Database.conn.execute(header)
        count = 0
        elo = 1000
        for row in result:
            count += 1
            elo = row[4]
        if count == 0:
            print("no results found, therefore ELO is default 1000")
            return elo
        #print(str(player_id) + " player elo: " + str(elo))
        return elo

