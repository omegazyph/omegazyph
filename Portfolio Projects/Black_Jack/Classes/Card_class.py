class Card:
    def __init__(self, suit, value):
        self.suit = suit  # Initialize the suit of the card
        self.value = value  # Initialize the value of the card

    def __repr__(self):
        return f"{self.value} of {self.suit}"  # Return a string representation of the card
