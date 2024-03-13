from Classes.Hand_class import *

class Dealer:
    def __init__(self):
        # Constructor method to initialize a Dealer object
        self.hand = Hand()  # Create a new Hand object for the dealer

    def add_card_to_hand(self, card):
        # Method to add a card to the dealer's hand
        self.hand.add_card(card)  # Call the add_card method of the Hand object to add the card to the hand

    def get_hand_value(self):
        # Method to get the value of the dealer's hand
        return self.hand.calculate_value()  # Call the calculate_value method of the Hand object to calculate the hand value
