"""
Date: 2026-01-08
Script Name: number_guesser.py
Author: omegazyph
Updated: 2026-01-08
Description: A simple object-oriented Python game where multiple players 
             submit guesses to match a randomly generated secret number.
"""

from random import randint

class NumberGuesser:
    """Class to manage player guesses and a secret random number."""
    
    def __init__(self, player_names):
        """
        Initializes the game with a list of players and a secret number.
        :param player_names: List of strings representing player names.
        """
        # Dictionary to store player names as keys and their guesses as values
        self.player_guesses = {}
        
        # Generate a random secret number between 1 and 10
        self.secret_number = randint(1, 10)
        
        # Populate the dictionary with players, defaulting their guess to -1
        for name in player_names:
            self.player_guesses[name] = -1

    def add_player_guess(self, name, guess):
        """
        Updates the guess for a specific player if they exist in the game.
        :param name: String name of the player.
        :param guess: Integer guess value.
        """
        if name in self.player_guesses:
            self.player_guesses[name] = guess
        else:
            # Feedback if a player name isn't recognized
            print(f"Error: '{name}' is not in the current game.")

    def print_answer(self):
        """Prints the secret number to the console."""
        print(f"\n{self.secret_number} is the secret number!")
    
    def print_guesses(self):
        """Iterates through all players and prints their current guess status."""
        print("--- Current Player Guesses ---")
        for player, guess in self.player_guesses.items():
            if guess != -1:
                print(f"{player} guessed: {guess}")
            else:
                print(f"{player} still needs to guess!")

# --- Main Execution ---

if __name__ == "__main__":
    # Initialize the game with a list of players
    game1 = NumberGuesser(["Thuy", "Joe", "Diya"])

    # Attempting to add guesses
    # Note: 'Roger' is not in the initial list, so the error check will trigger
    game1.add_player_guess("Roger", 10)
    game1.add_player_guess("Diya", 8)
    game1.add_player_guess("Thuy", 1)
    game1.add_player_guess("Joe", 5)

    # Display results
    game1.print_guesses()
    game1.print_answer()