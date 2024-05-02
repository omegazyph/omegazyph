"""
Battery Level Checker
by Wayne Stock
created on 2024-05-01

This program checks the battery level entered by the user and provides a corresponding message.

"""

# Get user input for battery level
user_input = int(input("Enter the battery level\n>> "))

# Check the battery level and provide appropriate messages
if user_input >= 1 and user_input <= 5:
    print("The battery is dead. Please charge it.")

elif user_input >= 5 and user_input <= 15:
    print("You have almost a dead battery. You can charge it.")

elif user_input >= 15 and user_input <= 25:
    print("Your battery is really low. Charge it.")

elif user_input >= 25 and user_input <= 45:
    print("You have a medium battery. I recommend you charge it.")

elif user_input >= 45 and user_input <= 60:
    print("Your battery is good, but don't use it too much!")

elif user_input >= 60 and user_input <= 80:
    print("Your battery is great. Use it!")

elif user_input >= 80 and user_input <= 100:
    print("Your battery is full.")

else:
    print("Can't determine the battery level.")
