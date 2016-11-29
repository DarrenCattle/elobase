'''
elobase
Darren Cattle
November 2016
'''

from src.Player import Player
from src.Database import Database

a = Player("A", 1200)
b = Player("B", 1200)
c = Player("C")

Player.disp()
a.win(b)
b.win(c)
c.win(a)

tic = Database("tic")

db = Database()
print("db = Database() success")
