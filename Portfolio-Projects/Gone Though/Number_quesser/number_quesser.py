#!/usr/bin/env python3
"""
==============================================================================
SCRIPT NAME:    number_quesser.py
DESCRIPTION:    A terminal-based guessing game where the player tries to 
                find a random number within a user-defined range.
AUTHOR:         omegazyph
DATE CREATED:   05-22-2025
DATE UPDATED:   01-05-2026
VERSION:        1.2
==============================================================================
"""

import random

def save_best_score(guesses):
    """Saves the lowest number of guesses (best score) to a file."""
    best_score = float('inf')
    try:
        with open("guess_score.txt", "r") as f:
            content = f.read().strip()
            if content:
                best_score = int(content)
    except (FileNotFoundError, ValueError):
        best_score = float('inf')

    if guesses < best_score:
        with open("guess_score.txt", "w") as f:
            f.write(str(guesses))
        print(f"🏆 NEW RECORD! Best score: {guesses} guesses.")
    else:
        print(f"Current Record to beat: {best_score} guesses.")

def main():
    """Main game logic for the Number Guesser."""
    print("====================================")
    print("      OMEGAZYPH NUMBER GUESSER")
    print("====================================\n")

    top_of_range = input("Type a number for the top of the range: ")

    # Checking if the input is a valid integer
    if top_of_range.isdigit():
        top_of_range = int(top_of_range)

        if top_of_range <= 0:
            print("Please type a number larger than 0 next time.")
            return
    else:
        print("Please type a number next time.")
        return

    # Generating a random number within the specified range
    random_number = random.randint(0, top_of_range)
    guesses = 0

    print(f"I'm thinking of a number between 0 and {top_of_range}...")

    # Starting a loop for the user to make guesses
    while True:
        guesses += 1
        user_guess = input("Make a guess: ")

        if user_guess.isdigit():
            user_guess = int(user_guess)
        else:
            print("Invalid input. Please type a numeric value.")
            continue

        # Comparing the user's guess with the random number
        if user_guess == random_number:
            print("\n✨ You got it!")
            break
        elif user_guess > random_number:
            print("You were above the number!")
        else:
            print("You were below the number!")

    print(f"It took you {guesses} guesses.")
    save_best_score(guesses)

if __name__ == "__main__":
    main()