import numpy as np


class AnalyticRecords:
    def __init__(self, pot, winloss, streak):
        self.pot = pot
        self.winloss = winloss
        self.streak = streak

    def get_pot_mean(self):
        return np.mean(self.pot)

    def get_pot_var(self):
        return np.var(self.pot)

    def get_winloss_mean(self):
        return np.mean(self.winloss)

    def get_winloss_var(self):
        return np.var(self.winloss)

    def get_streak_mean(self):
        return np.mean(self.streak)

    def get_streak_var(self):
        return np.var(self.streak)

    # calculate confidence interval
    def calc_ci(self, mean, z, var, n):
        ci_plus = mean + (z * np.sqrt(var/n))
        ci_minus = mean - (z * np.sqrt(var/n))
        return ci_minus, ci_plus
