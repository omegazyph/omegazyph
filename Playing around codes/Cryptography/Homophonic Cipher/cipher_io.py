"""
-------------------------------------------------------------------------
PROJECT  : Homophonic Cipher
FILE     : cipher_io.py
AUTHOR   : omegazyph
DATE     : 10/07/2025
UPDATED  : 12/29/2025
DESCRIPTION: Handles File I/O operations for the Homophonic Cipher.
             Includes automatic text wrapping for ciphertext output.
-------------------------------------------------------------------------
"""

import json
import random
import textwrap

# -------------------- I/O HELPER FUNCTIONS --------------------

def read_message_from_file(filepath):
    """Reads the entire content from a specified file."""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{filepath}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

def write_message_to_file(filepath, message, wrap=False):
    """
    Writes the given message string to a specified file.
    If wrap is True, it formats the text to 50 characters wide.
    """
    try:
        if wrap:
            message = textwrap.fill(message, width=50)
            
        with open(filepath, 'w') as f:
            f.write(message)
        print(f"Success! The result has been written to: '{filepath}'")
        return True
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")
        return False

# -------------------- CORE CIPHER FUNCTIONS --------------------

def load_cipher_map(filepath="cipher_map.json"):
    """Loads the substitution map from the JSON file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The key file '{filepath}' was not found.")
        return None

def encode_message(plaintext, cipher_map):
    """Encrypts the message using the polyalphabetic substitution map."""
    if not cipher_map or not plaintext:
        return ""

    ciphertext = []
    plaintext = plaintext.upper() 

    for char in plaintext:
        if char in cipher_map:
            substitutes = cipher_map[char]
            ciphertext.append(random.choice(substitutes))
        else:
            ciphertext.append(char)
            
    return "".join(ciphertext)

def create_reverse_map(cipher_map):
    """Creates a reverse map for decoding with length-sorted substitutes."""
    reverse_map = {}
    all_subs = []
    for plaintext_char, substitutes in cipher_map.items():
        for sub in substitutes:
            reverse_map[sub] = plaintext_char.upper()
            all_subs.append(sub)

    all_subs.sort(key=len, reverse=True)
    return reverse_map, all_subs

def decode_message(ciphertext, reverse_map, sorted_subs):
    """Decrypts the message using the reverse substitution map."""
    # Remove newlines before decoding so the pointer logic stays accurate
    ciphertext = ciphertext.replace('\n', '').replace('\r', '')
    
    plaintext = []
    i = 0
    N = len(ciphertext)
    
    while i < N:
        found = False
        for sub in sorted_subs:
            sub_len = len(sub)
            if ciphertext[i : i + sub_len] == sub:
                plaintext.append(reverse_map[sub])
                i += sub_len
                found = True
                break
        
        if not found:
            plaintext.append(ciphertext[i])
            i += 1

    return "".join(plaintext)

# -------------------- MAIN EXECUTION --------------------

if __name__ == "__main__":
    cipher_map = load_cipher_map()
    if not cipher_map:
        exit()

    rev_map, subs_list = create_reverse_map(cipher_map)

    print("\n--- File-Based Polyalphabetic Cipher Tool ---")
    
    while True:
        action = input("Do you want to (E)ncode or (D)ecode a file, or (Q)uit? ").strip().upper()

        if action == 'E':
            print("\n--- ENCODE ---")
            in_f = input("Enter the input text file name: ")
            out_f = input("Enter the output file name: ")
            
            p_text = read_message_from_file(in_f)
            if p_text is not None:
                encrypted = encode_message(p_text, cipher_map)
                # Apply wrapping for the ciphertext file
                write_message_to_file(out_f, encrypted, wrap=True)
        
        elif action == 'D':
            print("\n--- DECODE ---")
            in_f = input("Enter the input ciphertext file name: ")
            out_f = input("Enter the output file name: ")
            
            c_text = read_message_from_file(in_f)
            if c_text is not None:
                decrypted = decode_message(c_text, rev_map, subs_list)
                # No wrapping needed for decrypted plaintext
                write_message_to_file(out_f, decrypted, wrap=False)
            
        elif action == 'Q':
            print("\nCipher tool closed. Goodbye! 👋")
            break
            
        else:
            print("Invalid choice. Please enter E, D, or Q.")