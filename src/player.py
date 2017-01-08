import math
from src.database import Database

class Player:

    k_factor = 40
    r_factor = 400

    def __init__(self, i, n):
        self.id = i
        self.name = n

    def __str__(self):
        return 'ID: ' + str(self.id) + ", NAME: " + self.name

    def getPlayer(i):
        name = Database.getPlayerName(i)
        if name == 0:
            return None
        else:
            return Player(i, name)

    def createPlayer(player_name, pwd):
        i = Database.getFreshID("player_master")
        player = Player(i,player_name)
        Database.createPlayer(player, pwd)
        return Player.getPlayer(i)

    def win(self,PB,game_id):
        if(self.id==PB.id):
            return None
        r_a = Database.getElo(self.id,game_id)
        r_b = Database.getElo(PB.id,game_id)
        e_a = 1/(1+pow(10,(r_b-r_a)/Player.r_factor))
        e_b = 1/(1+pow(10,(r_a-r_b)/Player.r_factor))
        gain = math.ceil(Player.k_factor*(1-e_a))
        loss = math.ceil(Player.k_factor*(0-e_b))

        Database.createResult(game_id, self.id, r_a, r_a+gain, PB.id, r_b, r_b+loss)

        print(self.name + " has defeated " + PB.name)
        print(self.name + " +" + str(gain) + " " + str(r_a+gain))
        print(PB.name + " " + str(loss) + " " + str(r_b+loss))

    def lose(self, PB, game_id):
        PB.win(self, game_id)
