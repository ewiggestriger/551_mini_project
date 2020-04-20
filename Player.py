class Player:
    def __init__(self, pot, bet, wins, losses, win_streak, profit):
        self.pot = pot
        self.bet = bet
        self.wins = wins
        self.losses = losses
        self.win_streak = win_streak
        self.profit = profit

    def get_pot(self):
        return self.pot

    def get_bet(self):
        return self.bet

    def get_wins(self):
        return self.wins

    def get_losses(self):
        return self.losses

    def get_win_streak(self):
        return self.win_streak

    def get_profit(self):
        return self.profit

    def set_pot(self, p):
        self.pot += p

    def set_bet(self, b):
        self.bet += b

    def reset_bet(self, r):
        self.bet = r

    def set_wins(self, w):
        self.wins += w

    def set_losses(self, l):
        self.losses += l

    def set_win_streak(self, ws):
        self.win_streak += ws

    def reset_win_steak(self):
        self.win_streak = 0

    def set_profit(self, pr):
        self.profit = pr

    def reset_profit(self):
        self.profit = 0
