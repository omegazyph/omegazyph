"""
-------------------------------------------------------------------------
PROJECT  : Homophonic Cipher
FILE     : encode.py
AUTHOR   : omegazyph
DATE     : 10/07/2025
UPDATED  : 12/29/2025
DESCRIPTION: Encodes plaintext by mapping single characters to multiple 
             possible substitutes defined in a JSON cipher map.
-------------------------------------------------------------------------
"""

import json
import random

def load_cipher_map(filename="cipher_map.json"):
    """Loads the homophonic cipher map from a JSON file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file '{filename}' is not valid JSON.")
        return None

def homophonic_encode(plaintext, cipher_map):
    """
    Encrypts plaintext using the homophonic cipher map.
    - Converts all letters to uppercase for lookup.
    - Selects a random symbol for each letter (Homophonic Substitution).
    - Keeps non-alphabetic characters (like spaces) as is.
    """
    if not cipher_map:
        return "Encoding failed: Cipher map not loaded."

    ciphertext = []
    
    for char in plaintext:
        # Convert character to uppercase to match the JSON map keys
        upper_char = char.upper()
        
        if upper_char in cipher_map:
            # Randomly select one substitute from the list to flatten frequency
            substitute = random.choice(cipher_map[upper_char])
            ciphertext.append(substitute)
        else:
            # Keep punctuation, spaces, and numbers original
            ciphertext.append(char)
            
    return "".join(ciphertext)

# --- Main execution block ---
if __name__ == "__main__":
    # 1. Load the map
    mapping = load_cipher_map()
    
    if mapping:
        # 2. Get user input
        user_input = input("Enter the text to encode: ")
        
        # 3. Perform encoding
        encoded_text = homophonic_encode(user_input, mapping)
        
        # 4. Print results
        print("\n--- Ciphertext Output ---")
        print(encoded_text)
        print("-------------------------\n")