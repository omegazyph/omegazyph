import random

user_wins = 0  # Variable to track the number of times the user wins
computer_wins = 0  # Variable to track the number of times the computer wins

options = ["rock", "paper", "scissors"]  # List of available options for the game

# Main game loop
while True:
    user_input = input("Type Rock/Paper/Scissors or Q to quit :> ").lower()  # Getting user input
    
    if user_input == "q":  # Quitting the game if the user input is 'q'
        break

    if user_input not in options:  # Skipping the current iteration if the user input is not valid
        continue

    random_number = random.randint(0, 2)  # Generating a random number to represent the computer's choice
    computer_pick = options[random_number]  # Getting the computer's pick based on the random number
    
    print("Computer picked", computer_pick + ".")  # Displaying the computer's pick

    # Determining the winner of the round
    if user_input == "rock" and computer_pick == "scissors":
        print("You win!")
        user_wins += 1  # Incrementing user wins count
        
    elif user_input == "paper" and computer_pick == "rock":
        print("You win!")
        user_wins += 1
        
    elif user_input == "scissors" and computer_pick == "paper":
        print("You win!")
        user_wins += 1
        
    else:
        print("You Lost!")
        computer_wins += 1  # Incrementing computer wins count

# Printing the final results
print("You won", user_wins, "times.")
print("The computer won", computer_wins, "times.")
print("Goodbye!")
