'''
calculate_centennial_year
by Wayne Stock
Started on: 10/28/2018
Description: This script asks the user for their name and age, then calculates and prints the year they will turn 100 years old.
'''

# Ask the user for their name
name = input("Give me your name: ")

# Ask the user for their age and convert it to an integer
age = int(input("Give me your age: "))

# Ask the user for the current year and convert it to an integer
year = int(input("What is the current year: "))

# Calculate the year the user will turn 100
end_year = (year - age) + 100

# Print out a message with the user's name and the year they will turn 100
print(f"{name} will be 100 years old in the year {end_year}.")
