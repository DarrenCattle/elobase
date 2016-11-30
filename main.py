'''
elobase
Darren Cattle
November 2016
'''

from src.Player import Player
from src.Database import Database

#a = Player("A")
#b = Player("B")
#c = Player("C")

#a.disp()
#a.win(b)
#b.win(c)
#c.win(a)

p = Player
db = Database()

print("p = Player() success")
print("db = Database() success")

a = p.getPlayer(1)
b = p.getPlayer(2)
