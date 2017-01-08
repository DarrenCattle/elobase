'''
elobase
Darren Cattle
November 2016
'''

from src.database import Database
from src.player import Player

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

d = Database should only call createGame

1. d.createGame(game_name)

future methods?

1. p.deletePlayer(player_id, game_id)
2. p.renamePlayer(player_name) -> p.getPlayer -> p.renamePlayer
3. p.deleteGame


'''

p = Player
print("p = Player success")
d = Database
print("d = Database success")

def setup():
    d.createPlayerMaster()
    d.createGameMaster()
    a = p.createPlayer("a","a")
    b = p.createPlayer("b","b")

#a = p.getPlayer(1)
#b = p.getPlayer(2)

#print(a)
#print(b)
