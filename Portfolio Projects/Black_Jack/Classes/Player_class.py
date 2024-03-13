from Classes.Hand_class import *

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()

    def add_card_to_hand(self, card):
        self.hand.add_card(card)

    def get_hand_value(self):
        return self.hand.calculate_value()

class Dealer:
    def __init__(self):
        self.hand = Hand()

    def add_card_to_hand(self, card):
        self.hand.add_card(card)

    def get_hand_value(self):
        return self.hand.calculate_value()