'''
Age Calculation Program
by Wayne Stock
Created on: 2018-09-04
updated on: 2024-08-14
Description: This script calculates the year when a person will turn 100 years old based on their current age. It provides 
three different methods for obtaining the current year: using the current date, a fixed year, or user input.
'''

import datetime

# Method 1: Using the current year from the system date
def method_1():
    name = input("What is your name: ")
    age = int(input("How old are you: "))
    this_year = int(datetime.date.today().strftime("%Y"))
    year = str((this_year - age) + 100)
    print(f"{name} will be 100 years old in the year {year}")

# Method 2: Using a fixed year (2018) for demonstration
def method_2():
    name = input("What is your name: ")
    age = int(input("How old are you: "))
    year = str((2018 - age) + 100)
    print(f"{name} will be 100 years old in the year {year}")

# Method 3: Using user input for the current year
def method_3():
    name = input("What is your name: ")
    age = int(input("How old are you: "))
    this_year = int(input("What year is it? : "))
    year = str((this_year - age) + 100)
    print(f"{name} will be 100 years old in the year {year}")

# Choose which method to use by calling the appropriate function
if __name__ == "__main__":
    # Uncomment the method you want to use:
    method_1()
    # method_2()
    # method_3()
    pass
