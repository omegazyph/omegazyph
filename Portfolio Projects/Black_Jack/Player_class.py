###################################
# BlackJack
# By Wayne Stock
# Started 2024-03-12
# It is the game of 21 playing aginst the dealer
################################################

import random


class Player:
    def __init__(self, input_name, input_bet):
        self.name = input_name
        self.bet = input_bet
        self.account = 0

    def add_money(self):
        choice = input("{name} would you like to add more money to the table:\n>> ".format(name = self.name).lower())
        if choice == "yes":
            add = int(input("{name} How much would you like to bring to the table:\n>> ".format(name = self.name)))
            add += self.account
        else:
            print("{name} you need money to play".format(name = self.name))

    def betting(self):
        money = int(input("{name} How much would you like to Bet:\n>> ".format(name = self.name)))
    

        game = int(input("choose a number 1 or 2:\n>> "))
        if game == 1: # will add money to the account
            print("YOU WIN")
            add = money + money *2
            self.account += add
            
        elif game == 2:
            print("Sorry you lose")
            self.account -= money
            



    def __repr__(self):
        return "{name} has {money} left on the table.".format(name = self.name, money = self.account)




#player info
new_player = Black_jack("Player_1", 0)
new_player.add_money()
new_player.betting()
print(repr(new_player))

'''
player2 = Player("player_2", 0)
player2.add_money()
print(repr(player2))
'''
