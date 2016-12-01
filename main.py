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

'''
Only use Player methods which will call Database() other than createMaster()

p = Player can call 4 methods

1. a = p.createPlayer(player_name)
2. b = p.getPlayer(player_id)
3. a.win(b,1)
4. a.lose(b,1)

'''

p = Player
print("p = Player() success")

a = p.getPlayer(1)
b = p.getPlayer(2)
