###################################
# BlackJack
# By Wayne Stock
# Started 2024-03-12
# It is the game of 21 playing aginst the dealer
################################################


class Player:
    def __init__(self, input_name, input_bet):
        self.name = input_name
        self.bet = input_bet
        self.account = []

    def add_money(self):
        add = int(input("{name} How much would you like to bring to the table:\n>> ".format(name = self.name)))
        self.account.append(add)

    def __repr__(self):
        return "{name} has {money} left on the table.".format(name = self.name, money = self.account)

#player info
new_player = Player("Player_1", 0)
new_player.add_money()
print(repr(new_player))

player2 = Player("player_2", 0)
player2.add_money()
print(repr(player2))