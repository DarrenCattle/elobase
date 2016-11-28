import os
import sqlite3

class Database:

    conn = sqlite3.connect('elobase.db')
    games = []

    print("Opened elobase successfully")

    def createGame(self, name):
        self.name = name
        query_string = "CREATE TABLE " + name + '''(ID INT PRIMARY KEY     NOT NULL,
        NAME           TEXT    NOT NULL,
        DATA           TEXT    NOT NULL,
        RECORD         TEXT    NOT NULL,
        GAMES          INT     NOT NULL,
        RATING         INT     NOT NULL);'''
        Database.conn.execute(query_string)

    def getDatabase(self):


    print("Table created successfully")
