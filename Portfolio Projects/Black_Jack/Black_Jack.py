###################################
# BlackJack
# By Wayne Stock
# Started 2024-03-12
# It is the game of 21 playing aginst the dealer
################################################

import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = 0
        num_aces = 0
        for card in self.cards:
            if card.rank.isdigit():
                value += int(card.rank)
            elif card.rank in ['Jack', 'Queen', 'King']:
                value += 10
            else:  # Ace
                num_aces += 1
                value += 11  # Default to 11

        # Adjust Ace values if necessary
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1

        return value

class Blackjack:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

    def deal_initial_cards(self):
        self.player_hand.add_card(self.deck.draw_card())
        self.player_hand.add_card(self.deck.draw_card())
        self.dealer_hand.add_card(self.deck.draw_card())
        self.dealer_hand.add_card(self.deck.draw_card())

    def hit(self, hand):
        hand.add_card(self.deck.draw_card())

    def is_bust(self, hand):
        return hand.get_value() > 21

    def play(self):
        print("Welcome to Blackjack!")

        self.deal_initial_cards()

        print("Player's Hand:")
        self.print_hand(self.player_hand)

        while True:
            choice = input("Do you want to hit or stand? (h/s): ").lower()
            if choice == 'h':
                self.hit(self.player_hand)
                print("Player's Hand:")
                self.print_hand(self.player_hand)
                if self.is_bust(self.player_hand):
                    print("You bust! Dealer wins.")
                    return
            elif choice == 's':
                break
            else:
                print("Invalid choice! Please enter 'h' to hit or 's' to stand.")

        print("\nDealer's Hand:")
        self.print_hand(self.dealer_hand)

        while self.dealer_hand.get_value() < 17:
            self.hit(self.dealer_hand)
            print("Dealer's Hand:")
            self.print_hand(self.dealer_hand)
            if self.is_bust(self.dealer_hand):
                print("Dealer busts! You win.")
                return

        player_score = self.player_hand.get_value()
        dealer_score = self.dealer_hand.get_value()

        if player_score > dealer_score:
            print("You win!")
        elif player_score < dealer_score:
            print("Dealer wins!")
        else:
            print("It's a tie!")

    def print_hand(self, hand):
        for card in hand.cards:
            print(card)

if __name__ == "__main__":
    game = Blackjack()
    game.play()

