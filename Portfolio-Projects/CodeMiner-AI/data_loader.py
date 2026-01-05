"""
Script Name: data_loader.py
Author: omegazyph
Created: 2026-01-05
Last Updated: 2026-01-05
Description: Auto-learning data loader that reads real Python files 
             to build a massive knowledge base for the AI.
"""
import os

def load_sample_data():
    # Start with our basic instructions
    base_data = """
# Task: Multiply two numbers
def multiply(a, b):
    return a * b

# Task: Power of a number
def power(a, b):
    return a ** b
"""
    # Create a folder called 'my_code' if it doesn't exist
    if not os.path.exists("my_code"):
        os.makedirs("my_code")
        print("--- Created 'my_code' folder. Put your .py files there! ---")
    
    # Read every .py file in that folder and add it to the brain
    extra_code = ""
    for file in os.listdir("my_code"):
        if file.endswith(".py"):
            with open(os.path.join("my_code", file), "r") as f:
                extra_code += f"\n# Task: Code from {file}\n" + f.read() + "\n"
    
    return base_data + extra_code