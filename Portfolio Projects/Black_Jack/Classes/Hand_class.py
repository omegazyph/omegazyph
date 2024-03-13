class Hand:
    def __init__(self):
        # Constructor method to initialize a Hand object
        self.cards = []  # Initialize an empty list to store the cards in the hand

    def add_card(self, card):
        # Method to add a card to the hand
        self.cards.append(card)  # Append the given card to the list of cards in the hand

    def calculate_value(self):
        # Method to calculate the total value of the hand
        value = 0  # Initialize a variable to store the total value of the hand
        num_aces = 0  # Initialize a variable to count the number of aces in the hand
        for card in self.cards:
            if card.value.isdigit():
                # If the card value is a digit, add its integer value to the total value
                value += int(card.value)
            elif card.value in ['Jack', 'Queen', 'King']:
                # If the card value is a face card (Jack, Queen, or King), add 10 to the total value
                value += 10
            else:  # Ace
                # If the card value is an Ace, increment the number of aces and add 11 to the total value
                num_aces += 1
                value += 11
        # Adjust the value if there are aces and the total value is greater than 21
        while value > 21 and num_aces:
            # If the total value is greater than 21 and there are aces in the hand, decrement the total value by 10 for each ace
            value -= 10
            num_aces -= 1
        return value  # Return the total value of the hand
