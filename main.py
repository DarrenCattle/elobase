'''
elobase
Darren Cattle
November 2016
'''

from src.Player import Player

p1 = Player("A", 1200)
p2 = Player("B", 1200)
p3 = Player("C")

Player.disp()
p1.win(p2)
p2.lose(p1)
Player.disp()