import math
from src.Database import Database

class Player:

    k_factor = 32
    r_factor = 400
    player_list = []

    def __init__(self, n=None, e=None):
        self.name = n if n is not None else ""
        self.elo = e if e is not None else 1000
        self.history = []
        Player.player_list.append(self)
        Database.insertPlayer("pin",self)

    def __str__(self):
        return 'Name: ' + self.name + ', Elo: ' + str(self.elo)

    def disp():
        for x in Player.player_list:
            print('Name: ' + x.name + ', Elo: ' + str(x.elo))

    def win(self,PB):
        r_a = self.elo
        r_b = PB.elo
        e_a = 1/(1+pow(10,(r_b-r_a)/Player.r_factor))
        e_b = 1/(1+pow(10,(r_a-r_b)/Player.r_factor))
        gain = math.ceil(Player.k_factor*(1-e_a))
        loss = math.ceil(Player.k_factor*(0-e_b))
        self.elo += gain
        PB.elo += loss
        print(self.name + " has defeated " + PB.name)
        print(self.name + " +" + str(gain) + " " + str(self.elo))
        print(PB.name + " " + str(loss) + " " + str(PB.elo))
        Database.updateRating("pin",self)
        Database.updateRating("pin",PB)

    def lose(self,PB):
        PB.win(self)