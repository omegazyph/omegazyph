# Importing necessary classes from separate files
from Classes.Deck_class import *
from Classes.Player_class import *
from Classes.Dealer_class import *

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
            print(f"You drew: {player.hand.cards[-1]}")  # Display the drawn card
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
        print(f"Dealer drew: {dealer.hand.cards[-1]}")  # Display the drawn card
        print(f"Dealer's hand value is now: {dealer.get_hand_value()}")  # Display the updated hand value
        if dealer.get_hand_value() > 21:  # Check if dealer busts
            print("Dealer busted! You win.")
            return False
    print("Dealer stands.")
    return True

# Function to start the blackjack game
def blackjack_game():
    player_name = input("Enter your name: ")  # Prompt the player to enter their name
    player = Player(player_name)  # Create a player object
    dealer = Dealer()  # Create a dealer object
    deck = Deck()  # Create a deck object
    deck.shuffle()  # Shuffle the deck

    # Deal initial cards
    deal_initial_cards(deck, player, dealer)

    # Show initial hands
    print(f"\n{player.name}'s hand: {player.hand.cards[0]}, {player.hand.cards[1]}")  # Display player's hand
    print(f"Dealer's hand: {dealer.hand.cards[0]}, <hidden>")  # Display dealer's hand with one card hidden

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
        print(f"{player.name} wins with a hand value of {player_score}!")
    elif player_score < dealer_score:  # Dealer wins
        print(f"Dealer wins with a hand value of {dealer_score}.")
    else:  # It's a tie
        print("It's a tie!")

# Start the game
blackjack_game()
