class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def calculate_value(self):
        value = 0
        num_aces = 0
        for card in self.cards:
            if card.value.isdigit():
                value += int(card.value)
            elif card.value in ['Jack', 'Queen', 'King']:
                value += 10
            else:  # Ace
                num_aces += 1
                value += 11
        # Adjust the value if there are aces and the total value is greater than 21
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1
        return value
