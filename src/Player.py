import math
from src.Database import Database

class Player:

    k_factor = 32
    r_factor = 400

    def __init__(self, n=None):
        self.name = n if n is not None else ""
        self.id = Database.getFreshID("player")
        Database.createPlayer(self)

    def __str__(self):
        return 'Name: ' + self.name + ', Elo: ' + str(self.elo)

    def disp(self):
        print('Name: ' + self.name + ', ID: ' + self.id)

    def win(self,PB,game_id):
        r_a = Database.getElo(self.id)
        r_b = Database.getElo(PB.id)
        e_a = 1/(1+pow(10,(r_b-r_a)/Player.r_factor))
        e_b = 1/(1+pow(10,(r_a-r_b)/Player.r_factor))
        gain = math.ceil(Player.k_factor*(1-e_a))
        loss = math.ceil(Player.k_factor*(0-e_b))

        instance_id = Database.createInstance(self.id,PB.id,game_id)
        Database.createResult(game_id, instance_id, self.id, r_a+gain)
        Database.createResult(game_id, instance_id, PB.id, r_b+loss)

        print(self.name + " has defeated " + PB.name)
        print(self.name + " +" + str(gain) + " " + str(r_a+gain))
        print(PB.name + " " + str(loss) + " " + str(r_b+loss))

    def lose(self, PB, game_id):
        PB.win(self, game_id)
