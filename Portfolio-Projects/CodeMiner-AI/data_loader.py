"""
Script Name: data_loader.py
Author: omegazyph
Created: 2026-01-05
Last Updated: 2026-01-05
Description: Auto-learning data loader with UTF-8 support to prevent 
             UnicodeDecodeErrors when reading local files.
"""
import os

def load_sample_data():
    base_data = """
# Task: Multiply two numbers
def multiply(a, b):
    return a * b

# Task: Power of a number
def power(a, b):
    return a ** b
"""
    if not os.path.exists("my_code"):
        os.makedirs("my_code")
        print("--- Created 'my_code' folder. Put your .py files there! ---")
    
    extra_code = ""
    for file in os.listdir("my_code"):
        if file.endswith(".py"):
            # ADDED: encoding="utf-8" and errors="ignore" for safety
            try:
                with open(os.path.join("my_code", file), "r", encoding="utf-8", errors="ignore") as f:
                    extra_code += f"\n# Task: Code from {file}\n" + f.read() + "\n"
            except Exception as e:
                print(f"--- Skipping {file} due to error: {e} ---")
    
    return base_data + extra_code