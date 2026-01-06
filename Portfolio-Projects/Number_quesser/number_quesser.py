import random  # Importing the random module to generate random numbers

# Asking the user to input a number
top_of_range = input("Type a number: ")  

# Checking if the input is a valid integer
if top_of_range.isdigit():  
    top_of_range = int(top_of_range)  # Converting the input to an integer

    # Checking if the input number is greater than 0
    if top_of_range <= 0:  
        print("Please type a number larger than 0 next time.")
        quit()  # Exiting the program if the input is not valid
else:
    print("Please type a number next time.")
    quit()  # Exiting the program if the input is not valid

# Generating a random number within the specified range
random_number = random.randint(0, top_of_range)  
guesses = 0  # Initializing a variable to count the number of guesses

# Starting a loop for the user to make guesses
while True:  
    guesses += 1  # Incrementing the guess count for each iteration
    user_guess = input("Make a guess: ")  # Asking the user to make a guess

    # Checking if the user's guess is a valid integer
    if user_guess.isdigit():  
        user_guess = int(user_guess)  # Converting the user's guess to an integer
    else:
        print("Please type a number next time.")
        continue  # Skipping the rest of the loop iteration if the input is not valid

    # Comparing the user's guess with the random number
    if user_guess == random_number:
        print("You got it!")  # Printing a message if the guess is correct
        break  # Exiting the loop if the guess is correct
    elif user_guess > random_number:
        print("You were above the number!")  # Printing a message if the guess is too high
    else:
        print("You were below the number!")  # Printing a message if the guess is too low

# Printing the number of guesses it took the user to guess the correct number
print("You got it in", guesses, "guesses")
