#!/usr/bin/env python3
"""
==============================================================================
SCRIPT NAME:    rock_paper_scissors.py
DESCRIPTION:    A terminal-based Rock, Paper, Scissors game with name tracking,
                score counting, and clipboard result sharing.
AUTHOR:         omegazyph
DATE CREATED:   05-22-2025
DATE UPDATED:   2026-01-05
VERSION:        1.1
==============================================================================
"""

import random
import tkinter as tk  # Used for the clipboard function

def copy_to_clipboard(text):
    """Copies the final game stats to the system clipboard."""
    root = tk.Tk()
    root.withdraw()  # Keeps the main window hidden
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()  # Required to ensure text stays in clipboard
    root.destroy()
    print("\n📋 Match summary copied to clipboard!")

def main():
    """Main game logic for Rock Paper Scissors."""
    print("====================================")
    print("    OMEGAZYPH ROCK PAPER SCISSORS")
    print("====================================\n")

    # Asking for the player's name for personalized scoring
    player_name = input("Enter your name: ").strip()
    if not player_name:
        player_name = "Player 1"

    user_wins = 0  # Track user score
    computer_wins = 0  # Track computer score
    options = ["rock", "paper", "scissors"]

    print(f"Hello {player_name}! Let's begin. (Type Q to quit)")

    # Main game loop
    while True:
        # Getting user input and converting to lowercase for comparison
        user_input = input("\nType Rock/Paper/Scissors or Q to quit :> ").lower()
        
        # Exit condition
        if user_input == "q":
            break

        # Input validation: check if the choice exists in our list
        if user_input not in options:
            print("Invalid choice. Please pick Rock, Paper, or Scissors.")
            continue

        # Generating the computer's choice
        random_number = random.randint(0, 2)
        computer_pick = options[random_number]
        
        print(f"Computer picked {computer_pick}.")

        # Determining the winner of the round
        if user_input == computer_pick:
            print("🤝 It's a tie!")

        elif user_input == "rock" and computer_pick == "scissors":
            print("✨ You win!")
            user_wins += 1
            
        elif user_input == "paper" and computer_pick == "rock":
            print("✨ You win!")
            user_wins += 1
            
        elif user_input == "scissors" and computer_pick == "paper":
            print("✨ You win!")
            user_wins += 1
            
        else:
            print("❌ You Lost!")
            computer_wins += 1

    # Printing the final session results
    print("\n" + "="*30)
    print(f"FINAL STATS FOR {player_name.upper()}")
    print(f"Your Wins: {user_wins}")
    print(f"Computer Wins: {computer_wins}")
    print("="*30)

    # Format result string and copy to clipboard
    result_text = f"{player_name} won {user_wins} times against the computer!"
    copy_to_clipboard(result_text)
    print("Goodbye!")

if __name__ == "__main__":
    main()