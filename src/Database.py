import os
import sqlite3

class Database:

    conn = sqlite3.connect('elobase.db')

    print("Opened elobase successfully")

    conn.execute('''CREATE TABLE COMPANY
       (ID INT PRIMARY KEY     NOT NULL,
       NAME           TEXT    NOT NULL,
       AGE            INT     NOT NULL,
       ADDRESS        CHAR(50),
       SALARY         REAL);''')

    print("Table created successfully")
