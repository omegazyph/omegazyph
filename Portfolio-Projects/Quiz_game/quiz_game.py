# Welcome message
print("Welcome to my computer quiz!")

# Asking if the player wants to play
playing = input("Do you want to play? ")

# Exiting the program if the player doesn't want to play
if playing.lower() != "yes":
    quit()

# Starting the quiz
print("Okay! Let's play :)")
score = 0  # Initializing the score variable to keep track of correct answers

# Asking the first question
answer = input("What does CPU stand for? ")
if answer.lower() == "central processing unit":
    print("Correct!")  # Providing feedback for correct answer
    score += 1  # Incrementing the score for correct answer
else:
    print("Incorrect!")  # Providing feedback for incorrect answer

# Asking the second question
answer = input("What does GPU stand for? ")
if answer.lower() == "graphics processing unit":
    print("Correct!")
    score += 1
else:
    print("Incorrect!")

# Asking the third question
answer = input("What does RAM stand for? ")
if answer.lower() == "random access memory":
    print("Correct!")
    score += 1
else:
    print("Incorrect!")

# Asking the fourth question
answer = input("What does PSU stand for? ")
if answer.lower() == "power supply":
    print("Correct!")
    score += 1
else:
    print("Incorrect!")

# Displaying the final score
print(" You got " + str(score) + " questions correct")
print(" You got " + str((score/4)*100) + "%. correct")
