# Import random class
import random

class Number_Guesser:
  
  def __init__(self, player_names):
    self.player_guesses = {}


    # Adds names and -1 to player_guesses
    for name in player_names:
      self.player_guesses[name] = -1
      
    # Update to choose a random number
      self.secret_number = -1


#####################################################
  def add_player_guess(self, name, guess):
    # Fill in this method
    for name in Number_Guesser():
        print(name)
        
    
    
######################################################     
  def print_answer(self):
    print(str(self.secret_number), "is the secret number!")
    
  def print_guesses(self):
    for player in self.player_guesses.items():
      if player[1] != -1:
        print(player[0], "guessed", str(player[1]))
      else:
        print(player[0], "needs to guess!") 

game1 = Number_Guesser(["Thuy", "Joe", "Diya"])
game1.add_player_guess("Roger", 10)
game1.add_player_guess("Diya", 8)
game1.add_player_guess("Thuy", 1)
game1.add_player_guess("Joe", 5)
game1.print_guesses()
game1.print_answer()