"""
-------------------------------------------------------------------------
PROJECT  : Homophonic Cipher
FILE     : cipher_program.py
AUTHOR   : omegazyph
DATE     : 10/07/2025
UPDATED  : 12/29/2025
DESCRIPTION: The main controller for the Homophonic Cipher. 
             Supports interactive encoding and decoding using a JSON map.
-------------------------------------------------------------------------
"""

import json
import random

# -------------------- CORE FUNCTIONS --------------------

def load_cipher_map(filepath="cipher_map.json"):
    """Loads the substitution map from the JSON file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {filepath} was not found.")
        return None

def encode_message(plaintext, cipher_map):
    """Encrypts the message using the polyalphabetic substitution map."""
    if not cipher_map:
        return "Encryption failed: Cipher map not loaded."

    ciphertext = []
    # Convert message to uppercase to match map keys
    plaintext = plaintext.upper() 

    for char in plaintext:
        if char in cipher_map:
            # Randomly select one substitute from the list (Homophonic style)
            substitutes = cipher_map[char]
            ciphertext.append(random.choice(substitutes))
        else:
            # Keep spaces and punctuation as is
            ciphertext.append(char)
            
    return "".join(ciphertext)

def create_reverse_map(cipher_map):
    """
    Creates a reverse map for decoding: {substitute: original_letter}
    Sorts substitutes by length (longest first) to ensure accurate decoding.
    """
    reverse_map = {}
    all_subs = []
    for plaintext_char, substitutes in cipher_map.items():
        for sub in substitutes:
            reverse_map[sub] = plaintext_char.upper()
            all_subs.append(sub)

    # CRITICAL: Sort by length descending to match multi-char substitutes first
    all_subs.sort(key=len, reverse=True)
    
    return reverse_map, all_subs

def decode_message(ciphertext, reverse_map, sorted_subs):
    """Decrypts the message using the reverse substitution map and a pointer."""
    plaintext = []
    i = 0
    N = len(ciphertext)
    
    while i < N:
        found = False
        # Try to match the LONGEST possible substitute at the current position
        for sub in sorted_subs:
            sub_len = len(sub)
            
            if ciphertext[i : i + sub_len] == sub:
                plaintext.append(reverse_map[sub])
                i += sub_len
                found = True
                break
        
        if not found:
            # Handle non-ciphered characters
            plaintext.append(ciphertext[i])
            i += 1

    return "".join(plaintext)

# -------------------- MAIN EXECUTION --------------------

if __name__ == "__main__":
    # 1. Load the cipher map
    mapping = load_cipher_map()
    if not mapping:
        exit()

    # 2. Prepare the decoding tools
    rev_map, subs_list = create_reverse_map(mapping)

    print("\n--- Polyalphabetic Cipher Tool ---")
    
    while True:
        action = input("Do you want to (E)ncode, (D)ecode, or (Q)uit? ").strip().upper()

        if action == 'E':
            msg = input("Enter the message to ENCODE: ")
            encrypted = encode_message(msg, mapping)
            print(f"\nENCRYPTED MESSAGE: {encrypted}\n")
        
        elif action == 'D':
            msg = input("Enter the message to DECODE: ")
            decrypted = decode_message(msg, rev_map, subs_list)
            print(f"\nDECRYPTED MESSAGE: {decrypted}\n")
            
        elif action == 'Q':
            print("Cipher tool closed. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter E, D, or Q.")