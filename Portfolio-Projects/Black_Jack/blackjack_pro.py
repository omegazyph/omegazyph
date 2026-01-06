#!/usr/bin/env python3
"""
==============================================================================
SCRIPT NAME:    blackjack_pro.py
DESCRIPTION:    A terminal-based Blackjack game with ASCII art, persistent
                bankroll, and high-score tracking.
AUTHOR:         omegazyph
DATE CREATED:   05-22-2025
DATE UPDATED:   01-05-2026
VERSION:        2.5
==============================================================================
"""

import random

class Card:
    """Represents a single playing card with a suit and a value."""
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

class Hand:
    """Manages cards and calculates scores with Ace logic."""
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def calculate_value(self):
        """Calculates score, treating Aces as 1 or 11 based on total."""
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

class Deck:
    """Standard 52-card deck generator."""
    def __init__(self):
        self.cards = []
        self.create_deck()

    def create_deck(self):
        suits = ['♥', '♦', '♣', '♠']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(s, v) for s in suits for v in values]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        return None

class Participant:
    """Base class for shared hand logic."""
    def __init__(self, name):
        self.name = name
        self.hand = Hand()

    def reset_hand(self):
        self.hand = Hand()

    def get_hand_value(self):
        return self.hand.calculate_value()

class Player(Participant):
    """Player class with balance tracking."""
    def __init__(self, name, balance):
        super().__init__(name)
        self.balance = balance

def display_cards(*cards):
    """Renders cards side-by-side without trailing spaces."""
    lines = ["", "", "", "", "", "", ""]
    for idx, card in enumerate(cards):
        val = card.value if card else "?"
        s = card.suit if card else "?"
        card_art = [
            "┌───────┐",
            f"| {val:<2}    |",
            "|       |",
            f"|   {s}   |",
            "|       |",
            f"|    {val:>2} |",
            "└───────┘"
        ]
        for i in range(7):
            # Add a spacer only if it's not the last card to prevent MD009
            spacer = "  " if idx < len(cards) - 1 else ""
            lines[i] += card_art[i] + spacer
    return "\n".join(lines)

def save_high_score(name, score):
    """Persistent high score tracking."""
    high_score = 0
    try:
        with open("high_score.txt", "r") as f:
            content = f.read().strip()
            if ":" in content:
                high_score = int(content.split(":")[1])
    except (FileNotFoundError, ValueError, IndexError):
        high_score = 0
    if score > high_score:
        with open("high_score.txt", "w") as f:
            f.write(f"{name}:{score}")
        print(f"\n🏆 NEW HIGH SCORE: ${score}")

def play_round(player):
    """Logic for a single round of play."""
    deck = Deck()
    deck.shuffle()
    player.reset_hand()
    dealer_hand = Hand()
    while True:
        try:
            print(f"\nBalance: ${player.balance}")
            bet = int(input("Place your bet: $"))
            if 0 < bet <= player.balance:
                player.balance -= bet
                break
            print("Invalid bet.")
        except ValueError:
            print("Numbers only.")
    for _ in range(2):
        player.hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
    print(f"\nDealer shows:\n{display_cards(dealer_hand.cards[0])}[Hidden]")
    print(f"\nYour hand:\n{display_cards(*player.hand.cards)}")
    while player.get_hand_value() < 21:
        choice = input("(H)it or (S)tand? ").lower()
        if choice == 'h':
            card = deck.deal_card()
            player.hand.add_card(card)
            print(f"\nDrew:\n{display_cards(card)}Total: {player.get_hand_value()}")
            if player.get_hand_value() > 21:
                print("--- BUST ---")
                return
        else:
            break
    print(f"\nDealer reveal:\n{display_cards(*dealer_hand.cards)}")
    while dealer_hand.calculate_value() < 17:
        card = deck.deal_card()
        dealer_hand.add_card(card)
        print(f"Dealer draws:\n{display_cards(card)}")
    p_score = player.get_hand_value()
    d_score = dealer_hand.calculate_value()
    if d_score > 21 or p_score > d_score:
        print("WINNER!")
        player.balance += (bet * 2)
    elif p_score < d_score:
        print("LOSER.")
    else:
        print("PUSH.")
        player.balance += bet

def main():
    """Main game entry point."""
    print("====================================")
    print("      OMEGAZYPH BLACKJACK v2.5")
    print("====================================")
    name = input("Enter name: ")
    player = Player(name, 100)
    while player.balance > 0:
        play_round(player)
        save_high_score(player.name, player.balance)
        if player.balance <= 0:
            print("Out of cash!")
            break
        if input("\nPlay again? (y/n): ").lower() != 'y':
            break

if __name__ == "__main__":
    main()