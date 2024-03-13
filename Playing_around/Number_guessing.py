import random

def number_guessing_game():
    print("Welcome to the Number Guessing Game!")

    # Set the range for the random number (e.g., between 1 and 100)
    lower_limit = 1
    upper_limit = 100
    secret_number = random.randint(lower_limit, upper_limit)

    # Initialize the player's guess
    guess = None

    while guess != secret_number:
        try:
            # Get the player's guess
            guess = int(input(f"Guess the number between {lower_limit} and {upper_limit}: "))

            # Provide hints
            if guess < secret_number:
                print("Too low! Try again.")
            elif guess > secret_number:
                print("Too high! Try again.")
            else:
                print(f"Congratulations! You guessed the correct number: {secret_number}")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    number_guessing_game()
