class Dealer:
    def __init__(self, pot, wins, losses):
        self.pot = pot
        self.wins = wins
        self.losses = losses

    def get_pot(self):
        return self.pot

    def get_wins(self):
        return self.wins

    def get_losses(self):
        return self.losses

    def set_pot(self, p):
        self.pot += p

    def reset_bet(self, r):
        self.bet = r

    def set_wins(self, w):
        self.wins += w

    def set_losses(self, l):
        self.losses += l