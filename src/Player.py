import math

class Player:

    k_factor = 32
    r_factor = 400
    player_list = []

    def __init__(self, n=None, e=None):
        self.name = n if n is not None else ""
        self.elo = e if e is not None else 1000
        self.history = []
        Player.player_list.append(self)

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
        self.elo = r_a + math.ceil(Player.k_factor*(1-e_a))
        PB.elo = r_b + math.ceil(Player.k_factor*(0-e_b))
        print(self.elo, PB.elo)

    def lose(self,PB):
        PB.win(self)