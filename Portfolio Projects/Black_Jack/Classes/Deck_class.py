import random
from Classes.Card_class import *
from Classes.Deck_class_ASII import *
class Deck:
    def __init__(self):
        # Constructor method to initialize a Deck object
        self.cards = []  # Initialize an empty list to store cards
        self.create_deck()  # Call the create_deck method to populate the deck with cards

    def create_deck(self):
        # Method to create a standard deck of 52 cards
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']  # Define the suits of the cards
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']  # Define the values of the cards
        for suit in suits:
            for value in values:
                self.cards.append(Card(suit, value))  # Create a Card object for each combination of suit and value and add it to the deck

    def shuffle(self):
        # Method to shuffle the deck
        random.shuffle(self.cards)  # Shuffle the list of cards using the random.shuffle function

    def deal_card(self):
        # Method to deal a card from the deck
        if len(self.cards) > 0:
            return self.cards.pop()  # Remove and return the last card from the list of cards
        else:
            return None