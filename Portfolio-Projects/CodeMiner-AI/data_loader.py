"""
Script Name: data_loader.py
Author: omegazyph
Created: 2026-01-05
Last Updated: 2026-01-05
Description: Expanded Instruction-based training data to improve 
             task-to-code accuracy.
"""

def load_sample_data():
    return """
# Task: Greet a user
def greet(name):
    print("Hello " + name)

# Task: Add two numbers
def add(a, b):
    return a + b

# Task: Subtract two numbers
def subtract(a, b):
    return a - b

# Task: Multiply two numbers
def multiply(a, b):
    return a * b

# Task: Check if a number is even
def check_even(num):
    if num % 2 == 0:
        return True
    else:
        return False

# Task: Create a robot class
class Robot:
    def __init__(self, name):
        self.name = name
    def say_hi(self):
        print("I am " + self.name)

# Task: Loop ten times
for i in range(10):
    result = add(i, 5)
    print(result)

# Task: Square a number
def square(n):
    return n * n
"""