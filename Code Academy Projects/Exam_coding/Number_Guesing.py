# Importing randint function from the random module
from random import randint

class Number_Guesser:
  
  def __init__(self, player_names):
    # Initialize an empty dictionary to store player guesses
    self.player_guesses = {}
    
    # Initialize secret_number with a random number between 1 and 10
    self.secret_number = randint(1,10)
    
    # Add player names to player_guesses with initial guess as -1
    for name in player_names:
      self.player_guesses[name] = -1

#####################################################
  def add_player_guess(self, name, guess):
    # Method to add player guesses
    if name in self.player_guesses:
      self.player_guesses[name] = guess  # Update the guess for the player

######################################################     

  def print_answer(self):
    # Method to print the secret number
    print(str(self.secret_number), "is the secret number!")
    
  def print_guesses(self):
    # Method to print player guesses
    for player, guess in self.player_guesses.items():
      if guess != -1:
        print(player, "guessed", str(guess))
      else:
        print(player, "needs to guess!") 


# Create an instance of Number_Guesser
game1 = Number_Guesser(["Thuy", "Joe", "Diya"])

# Add player guesses
game1.add_player_guess("Roger", 10)
game1.add_player_guess("Diya", 8)
game1.add_player_guess("Thuy", 1)
game1.add_player_guess("Joe", 5)

# Print player guesses and the secret number
game1.print_guesses()
game1.print_answer()
