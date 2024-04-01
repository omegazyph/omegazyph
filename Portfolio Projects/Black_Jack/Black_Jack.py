import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit  # Initialize the suit of the card
        self.value = value  # Initialize the value of the card

class Hand:
    def __init__(self):
        self.cards = []  # Initialize an empty list to store the cards in the hand

    def add_card(self, card):
        self.cards.append(card)  # Append the given card to the list of cards in the hand

    def calculate_value(self):
        value = 0
        num_aces = 0
        for card in self.cards:
            if card.value.isdigit():
                value += int(card.value)
            elif card.value in ['J', 'Q', 'K']:
                value += 10
            else:
                num_aces += 1
                value += 11
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1
        return value

class Dealer:
    def __init__(self):
        self.hand = Hand()

    def add_card_to_hand(self, card):
        self.hand.add_card(card)

    def get_hand_value(self):
        return self.hand.calculate_value()

class Deck:
    def __init__(self):
        self.cards = []
        self.create_deck()

    def create_deck(self):
        suits = ['♥', '♦', '♣', '♠']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for suit in suits:
            for value in values:
                self.cards.append(Card(suit, value))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            return None

class Player:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance  # Initialize player's balance
        self.hand = Hand()

    def add_card_to_hand(self, card):
        self.hand.add_card(card)

    def get_hand_value(self):
        return self.hand.calculate_value()

# ASCII representation of cards
def display_cards(values1, suit1, values2, suit2):
    card1 = [
        f"┌───────┐",
        f"| {values1:<2}    |",
        f"|       |",
        f"|   {suit1}   |",
        f"|       |",
        f"|    {values1:>2} |",
        f"└───────┘"
    ]
    card2 = [
        f"┌───────┐",
        f"| {values2:<2}    |",
        f"|       |",
        f"|   {suit2}   |",
        f"|       |",
        f"|    {values2:>2} |",
        f"└───────┘"
    ]
    combined_cards = [""] * 7
    for i in range(7):
        combined_cards[i] = card1[i] + "   " + card2[i]
    return "\n".join(combined_cards)

# Function to deal initial cards to the player and the dealer
def deal_initial_cards(deck, player, dealer):
    for _ in range(2):
        player.add_card_to_hand(deck.deal_card())  # Deal a card to the player
        dealer.add_card_to_hand(deck.deal_card())  # Deal a card to the dealer

# Function to handle the player's turn
def player_turn(deck, player):
    while True:
        action = input("Do you want to hit or stand? (h/s): ").lower()  # Prompt the player for action
        if action == 'h':  # Player chooses to hit
            player.add_card_to_hand(deck.deal_card())  # Deal a card to the player
            print(f"You drew:\n{display_cards(player.hand.cards[-1].value, player.hand.cards[-1].suit, '', '')}")  # Display the drawn card
            print(f"Your hand value is now: {player.get_hand_value()}")  # Display the updated hand value
            if player.get_hand_value() > 21:  # Check if player busts
                print("You busted! Dealer wins.")
                return False
        elif action == 's':  # Player chooses to stand
            print("You chose to stand.")
            return True
        else:
            print("Invalid input. Please enter 'h' to hit or 's' to stand.")  # Invalid input

# Function to handle the dealer's turn
def dealer_turn(deck, dealer):
    print("\nDealer's turn:")
    while dealer.get_hand_value() < 17:  # Dealer hits until hand value reaches 17 or more
        dealer.add_card_to_hand(deck.deal_card())  # Deal a card to the dealer
        print(f"Dealer drew:\n{display_cards(dealer.hand.cards[-1].value, dealer.hand.cards[-1].suit, '', '')}")  # Display the drawn card
        print(f"Dealer's hand value is now: {dealer.get_hand_value()}")  # Display the updated hand value
        if dealer.get_hand_value() > 21:  # Check if dealer busts
            print("Dealer busted! You win.")
            return False
    print("Dealer stands.")
    return True

# Function to start the blackjack game
def blackjack_game():
    player_name = input("Enter your name: ")  # Prompt the player to enter their name
    player_balance = int(input("Enter your initial balance: "))  # Prompt the player to enter their initial balance
    player = Player(player_name, player_balance)  # Create a player object
    dealer = Dealer()  # Create a dealer object
    deck = Deck()  # Create a deck object
    deck.shuffle()  # Shuffle the deck

    # Betting
    while True:
        bet = int(input("Place your bet: "))  # Prompt the player to place a bet
        if bet <= player.balance:
            player.balance -= bet  # Deduct the bet amount from player's balance
            break
        else:
            print("Insufficient balance. Please place a lower bet.")

    # Deal initial cards
    deal_initial_cards(deck, player, dealer)

    # Show initial hands
    print(f"\n{player.name}'s hand:\n{display_cards(player.hand.cards[0].value, player.hand.cards[0].suit, player.hand.cards[1].value, player.hand.cards[1].suit)}")  # Display player's hand
    print(f"Dealer's hand:\n{display_cards(dealer.hand.cards[0].value, dealer.hand.cards[0].suit, '', '')}\n<hidden>")  # Display dealer's hand with one card hidden

    # Player's turn
    if not player_turn(deck, player):
        return

    # Dealer's turn
    if not dealer_turn(deck, dealer):
        return

    # Determine the winner
    player_score = player.get_hand_value()  # Get player's hand value
    dealer_score = dealer.get_hand_value()  # Get dealer's hand value
    print("\nGame over!")
    if player_score > dealer_score:  # Player wins
        player.balance += bet * 2  # Player wins double the bet amount
        print(f"{player.name} wins with a hand value of {player_score}!")
    elif player_score < dealer_score:  # Dealer wins
        print(f"Dealer wins with a hand value of {dealer_score}.")
    else:  # It's a tie
        player.balance += bet  # Return the bet amount to player
        print("It's a tie!")

    # Display player's balance
    print(f"{player.name}'s balance: {player.balance}")

# Start the game
blackjack_game()
