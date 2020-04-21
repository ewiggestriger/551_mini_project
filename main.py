# MSIM 551 Mini Project
# A monte carlo simulation of blackjack with 4 players
# to test blackjack betting strategies
# Steve Kostoff 17 April 2020

import random
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import Analysis
import Player
import Dealer

# initialize the simulation
cards = (2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11) # face cards are all value 10, except ace is 11
dealt = ([0])
n = 50  # number of games per simulation run
r = 10000  # number of simulation runs
alpha = 0.05  # precision 95% for confidence intervals
min_bet = 5
max_bet = 1000
profit = 0  # profit over betting, necessary for one of the strategies
d_pot = 50000
p1_pot = p2_pot = p3_pot = p4_pot = 500 # starting bankroll per player
d_wins = p1_wins = p2_wins = p3_wins = p4_wins = 0 # starting player win record
d_losses = p1_losses = p2_losses = p3_losses = p4_losses = 0 # starting player loss record
d_hand = ([0, 0]) # initial hands are two-cards
p1_hand = ([0, 0])
p2_hand = ([0, 0])
p3_hand = ([0, 0])
p4_hand = ([0, 0])
win_streak = 0  # default last win flag, necessary for one of the strategies
# create players
Player1 = Player.Player(p1_pot, min_bet, p1_wins, p1_losses, win_streak, profit)
Player2 = Player.Player(p2_pot, min_bet, p2_wins, p2_losses, win_streak, profit)
Player3 = Player.Player(p3_pot, min_bet, p3_wins, p3_losses, win_streak, profit)
Player4 = Player.Player(p4_pot, min_bet, p4_wins, p4_losses, win_streak, profit)
Dealer = Dealer.Dealer(d_pot, d_wins, d_losses)
# create data structures for output
martingale_pot = np.zeros(r)
manhattan_pot = np.zeros(r)
oscars_pot = np.zeros(r)
safe_pot = np.zeros(r)
dealers_pot = np.zeros(r)
martingale_winloss = np.zeros(r)
manhattan_winloss = np.zeros(r)
oscars_winloss = np.zeros(r)
safe_winloss = np.zeros(r)
martingale_streak = np.zeros(r)
manhattan_streak = np.zeros(r)
oscars_streak = np.zeros(r)
safe_streak = np.zeros(r)


# functions


# calculate z value
def calc_z_val(alpha):
    z = stats.norm.ppf(1 - alpha / 2)
    return z


# paired t method for system (strategy) comparison
def paired_z_method(array, alpha):
    mean = np.mean(array)
    z_val = stats.norm.ppf(1-alpha/2)
    variance = np.var(array)
    half_width = z_val * np.sqrt(variance/len(array))
    # construct CI
    ci_plus = mean + half_width
    ci_minus = mean - half_width
    print("The paired t confidence interval is between " + str(ci_minus) + " and " + str(ci_plus))
    if ci_minus <= 0 <= ci_plus:
        print("The null hypothesis is not rejected")
    else:
        print("The null hypothesis is rejected")


# deal the cards
def deal_cards(d_hand, p_hand1, p_hand2, p_hand3, p_hand4, cards):
    for x in range(2):
        d_hand[x] = random.choice(cards)
        p_hand1[x] = random.choice(cards)
        p_hand2[x] = random.choice(cards)
        p_hand3[x] = random.choice(cards)
        p_hand4[x] = random.choice(cards)


# player strategy (basic strategy)
# TODO develop soft ace mechanism
def basic_strategy(d_hand, p_hand, cards):
    # hit or stand defaults to True
    hit = True
    # print("Player hand is " + str(sum(p_hand)))
    # decision process
    while hit:
        if d_hand[1] < 4 and sum(p_hand) >= 13:
            hit = False
            # print("Player stands")
        elif 3 < d_hand[1] < 7 and sum(p_hand) >= 12:
            hit = False
            # print("Player stands")
        elif 7 <= d_hand[1] and sum(p_hand) > 16:
            hit = False
            # print("Player stands")
        else:
            # print("Player hit me")
            p_hand.append(random.choice(cards))
            # print("Player is dealt a " + str(p_hand[-1]))
            if sum(p_hand) == 21:
                # print("Player BLACKJACK")
                hit = False
            elif sum(p_hand) > 21:
                # print("Player is bust")
                hit = False
            else:
                hit = True
    # apply effects of bust, set hand to zero
    if sum(p_hand) > 21:
        del p_hand[2:]
        p_hand = ([0, 0])


# TODO fix dealer strategy
def d_strategy(d_hand, cards):
    # hit or stand defaults to True
    hit = True
    # print("Dealer hand is " + str(sum(d_hand)))
    # decision process
    while hit:
        if sum(d_hand) > 21:
            # print("Dealer busts")
            hit = False
        elif sum(d_hand) == 21:
            # print("Dealer BLACKJACK")
            hit = False
        elif 17 <= sum(d_hand) < 21:
            # print("Dealer stands.")
            hit = False
        else:
            d_hand.append(random.choice(cards))
            # print("Dealer is dealt a " + str(d_hand[-1]))
            hit = True
    # apply effects of bust
    if sum(d_hand) > 21:
        del d_hand[2:]
        p_hand = ([0, 0])


# betting strategies
def martingale_strategy(Player):
    # Martingale player follows Martingale strategy
    # get bet level and last win flag
    bet = Player.get_bet()
    win_streak = Player.get_win_streak()
    # apply strategy
    if win_streak < 1:
        bet *= 2
        Player.set_bet(bet)
    else:
        bet = min_bet
        Player.set_bet(bet)
    # check that maximum bet is not exceeded
    if Player.get_bet() > max_bet:
        Player.reset_bet(max_bet)


def oscars_grind_strategy(Player):
    # Oscar's grind players follows Oscar's grind strategy
    # get previous performance
    bet = Player.get_bet()
    win_streak = Player.get_win_streak()
    profit = Player.get_profit()
    # algorithm strives to make one unit (minimum bet) of profit in betting
    if profit < min_bet:
        if win_streak > 0:
            profit = profit + bet
            Player.set_profit(profit)
            if profit + bet + min_bet > min_bet:
                bet = min_bet - profit
                Player.set_bet(bet)
            else:
                bet = bet + min_bet
                Player.set_bet(bet)
        else:
            profit = profit - bet
            Player.set_profit(profit)
    # profit goal achieved, return to minimum bet
    else:
        bet = min_bet
        Player.reset_profit()
        Player.reset_bet(bet)
    # check that maximum bet is not exceeded
    if Player.get_bet() > max_bet:
        Player.reset_bet(max_bet)


def manhattan_strategy(Player):
    # manhattan player follows the 2-1-2 strategy
    win_streak = Player.get_win_streak()
    # first victory bet reduced to one unit
    if win_streak == 1:
        Player.set_bet(min_bet)
    # second and subsequent victories bets are trippled
    elif win_streak > 1:
        Player.set_bet(3 * min_bet)
    # player returns to default 2x bet setting if dealer wins
    else:
        Player.reset_bet(2 * min_bet)
    # check that maximum bet is not exceeded
    if Player.get_bet() > max_bet:
        Player.reset_bet(max_bet)


def safe_bet_strategy(Player):
    # safe bettor always bets the minimum bet
    Player.reset_bet(min_bet)


# assess game outcome
def assess_game_outcome(hand, d_hand, Player, Dealer):
    # assess player
    winner = None
    loser = None
    if sum(hand) == 0:
        # player automatically loses on a bust before dealer draws
        winner = d_hand
        loser = hand
    elif sum(d_hand) < sum(hand):
        winner = hand
        loser = d_hand
    else:
        winner = d_hand
        loser = hand

    # record wins and losses, and settle bets
    if winner == hand:
        # print("Player wins")
        Player.set_wins(1)
        Player.set_win_streak(1)
        Player.set_pot(Player.get_bet())
        Dealer.set_pot(-Player.get_bet())
    elif loser == hand:
        # print("Player loses")
        Player.set_losses(1)
        Player.set_win_streak(-1)
        Player.set_pot(-Player.get_bet())
        Dealer.set_pot(Player.get_bet())
    else:
        # will count as loss but pot is not deducted
        Player.set_losses(1)
        Player.set_win_streak(-1)
    # reset hands to zero
    del hand[2:]
    del d_hand[2:]


# run required number of simulation runs
for y in range(r):
    for x in range(n):
        # print("Round " + str(x))
        # conduct betting first
        martingale_strategy(Player1)
        manhattan_strategy(Player2)
        oscars_grind_strategy(Player3)
        safe_bet_strategy(Player4)
        # deal cards
        deal_cards(d_hand, p1_hand, p2_hand, p3_hand, p4_hand, cards)
        # each player plays hand according to strategy
        basic_strategy(d_hand, p1_hand, cards)
        basic_strategy(d_hand, p2_hand, cards)
        basic_strategy(d_hand, p3_hand, cards)
        basic_strategy(d_hand, p4_hand, cards)
        # dealer resolves his hand
        d_strategy(d_hand, cards)
        # assess each player's results and settle bets
        assess_game_outcome(p1_hand, d_hand, Player1, Dealer)
        assess_game_outcome(p2_hand, d_hand, Player2, Dealer)
        assess_game_outcome(p3_hand, d_hand, Player3, Dealer)
        assess_game_outcome(p4_hand, d_hand, Player4, Dealer)
    # record output variables
    martingale_pot[y] = Player1.get_pot()
    manhattan_pot[y] = Player2.get_pot()
    oscars_pot[y] = Player3.get_pot()
    safe_pot[y] = Player4.get_pot()
    dealers_pot[y] = Dealer.get_pot()
    martingale_winloss[y] = Player1.get_wins() - Player1.get_losses()
    manhattan_winloss[y] = Player2.get_wins() - Player2.get_losses()
    oscars_winloss[y] = Player3.get_wins() - Player3.get_losses()
    safe_winloss[y] = Player4.get_wins() - Player4.get_losses()
    martingale_streak[y] = Player1.get_win_streak()
    manhattan_streak[y] = Player2.get_win_streak()
    oscars_streak[y] = Player3.get_win_streak()
    safe_streak[y] = Player4.get_win_streak()
    # reset all players to defaults
    Player1.__init__(p1_pot, min_bet, p1_wins, p1_losses, win_streak, profit)
    Player2.__init__(p2_pot, min_bet, p2_wins, p2_losses, win_streak, profit)
    Player3.__init__(p3_pot, min_bet, p3_wins, p3_losses, win_streak, profit)
    Player4.__init__(p4_pot, min_bet, p4_wins, p4_losses, win_streak, profit)
    Dealer.__init__(d_pot, d_wins, d_losses)

# conduct analysis
# generate analysis objects
Martingale_Stats = Analysis.AnalyticRecords(martingale_pot, martingale_winloss, martingale_streak)
Manhattan_Stats = Analysis.AnalyticRecords(manhattan_pot, manhattan_winloss, manhattan_streak)
Oscar_Stats = Analysis.AnalyticRecords(oscars_pot, oscars_winloss, oscars_streak)
Safe_Stats = Analysis.AnalyticRecords(safe_pot, safe_winloss, safe_streak)
# part A - generate descriptive statistics and build confidence intervals
z_val = calc_z_val(alpha)
# mean, variance, and 95% confidence intervals for each strategy
# martingale strategy
print("Martingale strategy pot: mean " + str(Martingale_Stats.get_pot_mean()) + ", var " + str(Martingale_Stats.get_pot_var()))
print("Martingale strategy win/loss: mean " + str(Martingale_Stats.get_winloss_mean()) + ", var " + str(Martingale_Stats.get_winloss_var()))
print("Martingale strategy streak: mean " + str(Martingale_Stats.get_streak_mean()) + ", var " + str(Martingale_Stats.get_streak_var()))
print("Manhattan strategy pot: mean " + str(Manhattan_Stats.get_pot_mean()) + ", var " + str(Manhattan_Stats.get_pot_var()))
print("Manhattan strategy win/loss: mean " + str(Manhattan_Stats.get_winloss_mean()) + ", var " + str(Manhattan_Stats.get_winloss_var()))
print("Manhattan strategy streak: mean " + str(Manhattan_Stats.get_streak_mean()) + ", var " + str(Manhattan_Stats.get_streak_var()))
print("Oscar's Grind strategy pot: mean " + str(Oscar_Stats.get_pot_mean()) + ", var " + str(Oscar_Stats.get_pot_var()))
print("Oscar's Grind strategy win/loss: mean " + str(Oscar_Stats.get_winloss_mean()) + ", var " + str(Oscar_Stats.get_winloss_var()))
print("Oscar's Grind strategy streak: mean " + str(Oscar_Stats.get_streak_mean()) + ", var " + str(Oscar_Stats.get_streak_var()))
print("Safe strategy pot: mean " + str(Safe_Stats.get_pot_mean()) + ", var " + str(Safe_Stats.get_pot_var()))
print("Safe strategy win/loss: mean " + str(Safe_Stats.get_winloss_mean()) + ", var " + str(Safe_Stats.get_winloss_var()))
print("Safe strategy streak: mean " + str(Safe_Stats.get_streak_mean()) + ", var " + str(Safe_Stats.get_streak_var()))
print("Martingale strategy pot confidence interval " + str(Martingale_Stats.calc_ci(Martingale_Stats.get_pot_mean(), z_val, Martingale_Stats.get_pot_var(), r)))
print("Manhattan strategy pot confidence interval " + str(Manhattan_Stats.calc_ci(Martingale_Stats.get_pot_mean(), z_val, Manhattan_Stats.get_pot_var(), r)))
print("Oscar's Grind strategy pot confidence interval " + str(Oscar_Stats.calc_ci(Oscar_Stats.get_pot_mean(), z_val, Oscar_Stats.get_pot_var(), r)))
print("Safe strategy pot confidence interval " + str(Safe_Stats.calc_ci(Safe_Stats.get_pot_mean(), z_val, Safe_Stats.get_pot_var(), r)))
# part B - compare systems
# null hypothesis - no significant difference between strategies
compare_Mart_Man = np.subtract(martingale_pot, manhattan_pot)
compare_Mart_Osc = np.subtract(martingale_pot, oscars_pot)
compare_Mart_Saf = np.subtract(martingale_pot, safe_pot)
compare_Man_Osc = np.subtract(manhattan_pot, oscars_pot)
compare_Man_Saf = np.subtract(manhattan_pot, safe_pot)
compare_Osc_Saf = np.subtract(oscars_pot, safe_pot)
# change alpha value due to Bonferroni inequality
alpha = alpha / 6
print("Comparing Martingale Strategy with Manhattan Strategy:")
paired_z_method(compare_Mart_Man, alpha)
print("Comparing Martingale Strategy with Oscar's Grind Strategy:")
paired_z_method(compare_Mart_Osc, alpha)
print("Comparing Martingale Strategy with Safe Strategy:")
paired_z_method(compare_Mart_Saf, alpha)
print("Comparing Manhattan Strategy with Oscar's Grind Strategy:")
paired_z_method(compare_Man_Osc, alpha)
print("Comparing Manhattan Strategy with Safe Strategy:")
paired_z_method(compare_Man_Saf, alpha)
print("Comparing Oscar's Grind Strategy with Safe Strategy:")
paired_z_method(compare_Osc_Saf, alpha)
# part C - graphs and charts
# chart the pot winnings of each strategy against each other
fig, ax = plt.subplots()

ax.plot(martingale_pot, label='Martingale Winnings' )
ax.plot(manhattan_pot, label='Manhattan Winnings')
ax.plot(oscars_pot, label='Oscars Grind Winnings')
ax.plot(safe_pot, label='Safe Strategy Winnings')
ax.set(xlabel='Simulation Run', ylabel='Winnings in Dollars', title='Plot of Strategy Total Winnings')
ax.grid()
ax.legend()
fig.savefig("pot.png")
plt.show()

# chart the win/loss ratio of each strategy against each other
fig2, ax2 = plt.subplots()

ax2.plot(martingale_winloss, label='Martingale Win/Loss Balance')
ax2.plot(manhattan_winloss, label='Manhattan Win/Loss Balance')
ax2.plot(oscars_winloss, label='Oscars Grind Win/Loss Balance')
ax2.plot(safe_winloss, label='Safe Strategy Win/Loss Balance')
ax2.set(xlabel='Simulation Run', ylabel='Win/Loss Balance', title='Plot of Win/Loss Balance')
ax2.grid()
ax2.legend()
fig2.savefig("winloss.png")
plt.show()

# chart the win streak
fig3, ax3 = plt.subplots()
ax3.plot(martingale_streak, label='Martingale Win Streak Balance')
ax3.plot(manhattan_streak, label='Manhattan Win Streak Balance')
ax3.plot(oscars_streak, label='Oscars Grind Win Streak Balance')
ax3.plot(safe_streak, label='Safe Strategy Win Streak Balance')
ax3.set(xlabel='Simulation Run', ylabel='Win Streak Balance', title='Plot of Win Streak Balance')
ax3.grid()
ax3.legend()
fig3.savefig("streak.png")
plt.show()

# histogram of pot winnings
fig4, axs = plt.subplots(2,2)
axs[0,0].hist(martingale_pot, bins=20)
axs[0,0].set_title('Martingale')
axs[0,1].hist(manhattan_pot, bins=20, color='orange')
axs[0,1].set_title('Manhattan')
axs[1,0].hist(oscars_pot, bins=20, color='green')
axs[1,0].set_title('Oscars Grind')
axs[1,1].hist(safe_pot, bins=20, color='yellow')
axs[1,1].set_title('Safe Strategy')

for ax in axs.flat:
    ax.set(xlabel='Pot Winnings', ylabel='Number of Sim Runs')
    ax.grid()

fig4.savefig("histo.png")
plt.show()

