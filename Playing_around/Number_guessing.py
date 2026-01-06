"""
Number Guessing Game
by Wayne Stock
created on 2024-05-02

This program allows the user to play a number guessing game. The user has to guess a randomly generated number
within a specified range, and they have three attempts to guess it correctly.

"""

import random

def number_guessing_game():
    # Welcome message
    print("Welcome to the Number Guessing Game!")
    print("You have only 3 tries.")

    # Set the range for the random number (e.g., between 1 and 100)
    lower_limit = 1
    upper_limit = 100
    secret_number = random.randint(lower_limit, upper_limit)

    # Initialize variables
    guess = None
    number_of_tries = 0

    # Game loop
    while guess != secret_number:
        try:
            # Get the player's guess
            guess = int(input(f"Guess the number between {lower_limit} and {upper_limit}\n<: "))

            # Provide hints
            if guess < secret_number:
                print("Too low! Try again.")
                number_of_tries += 1
            elif guess > secret_number:
                print("Too high! Try again.")
                number_of_tries += 1
            else:
                print(f"Congratulations! You guessed the correct number: {secret_number}")

            # Check if the user has reached the maximum number of tries
            if number_of_tries == 3:
                print("You've reached the maximum number of tries. Start over and try again.")
                break

        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    number_guessing_game()
