# Python Script
# Author: Wayne Stock
# Date: 2018-09-05
# Description: This script prompts the user to enter a number and determines whether the number is odd or even.
# It does this by computing the modulus of the number with 2 and checking if the result is greater than 0.

# Prompt the user to enter a number
num = int(input("Enter a number: "))  # Convert input to an integer

# Compute the modulus of the number by 2
mod = num % 2

# Determine if the number is odd or even based on the modulus
if mod > 0:
    print("You picked an odd number.")
else:
    print("You picked an even number.")
