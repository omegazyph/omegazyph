# Calling the classes
from Classes.Deck_class import *
from Classes.Player_class import *
from Classes.Dealer_class import *

def deal_initial_cards(deck, player, dealer):
    for _ in range(2):
        player.add_card_to_hand(deck.deal_card())
        dealer.add_card_to_hand(deck.deal_card())

def player_turn(deck, player):
    while True:
        action = input("Do you want to hit or stand? (h/s): ").lower()
        if action == 'h':
            player.add_card_to_hand(deck.deal_card())
            print(f"You drew: {player.hand.cards[-1]}")
            print(f"Your hand value is now: {player.get_hand_value()}")
            if player.get_hand_value() > 21:
                print("You busted! Dealer wins.")
                return False
        elif action == 's':
            print("You chose to stand.")
            return True
        else:
            print("Invalid input. Please enter 'h' to hit or 's' to stand.")

def dealer_turn(deck, dealer):
    print("\nDealer's turn:")
    while dealer.get_hand_value() < 17:
        dealer.add_card_to_hand(deck.deal_card())
        print(f"Dealer drew: {dealer.hand.cards[-1]}")
        print(f"Dealer's hand value is now: {dealer.get_hand_value()}")
        if dealer.get_hand_value() > 21:
            print("Dealer busted! You win.")
            return False
    print("Dealer stands.")
    return True

def blackjack_game():
    player_name = input("Enter your name: ")
    player = Player(player_name)
    dealer = Dealer()
    deck = Deck()
    deck.shuffle()

    # Deal initial cards
    deal_initial_cards(deck, player, dealer)

    # Show initial hands
    print(f"\n{player.name}'s hand: {player.hand.cards[0]}, {player.hand.cards[1]}")
    print(f"Dealer's hand: {dealer.hand.cards[0]}, <hidden>")

    # Player's turn
    if not player_turn(deck, player):
        return

    # Dealer's turn
    if not dealer_turn(deck, dealer):
        return

    # Determine the winner
    player_score = player.get_hand_value()
    dealer_score = dealer.get_hand_value()
    print("\nGame over!")
    if player_score > dealer_score:
        print(f"{player.name} wins with a hand value of {player_score}!")
    elif player_score < dealer_score:
        print(f"Dealer wins with a hand value of {dealer_score}.")
    else:
        print("It's a tie!")

# Start the game
blackjack_game()
