from Classes.Hand_class import *

class Player:
    def __init__(self, name):
        # Constructor method to initialize a Player object
        self.name = name  # Assign the provided name to the player
        self.hand = Hand()  # Create a new Hand object for the player

    def add_card_to_hand(self, card):
        # Method to add a card to the player's hand
        self.hand.add_card(card)  # Call the add_card method of the Hand object to add the card to the player's hand

    def get_hand_value(self):
        # Method to get the value of the player's hand
        return self.hand.calculate_value()  # Call the calculate_value method of the Hand object to calculate the hand value
