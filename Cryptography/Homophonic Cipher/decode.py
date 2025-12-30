"""
-------------------------------------------------------------------------
PROJECT  : Homophonic Cipher
FILE     : decode.py
AUTHOR   : omegazyph
DATE     : 12/29/2025
DESCRIPTION: Decodes ciphertext back into plaintext using the 
             reverse-mapped values from the JSON cipher map.
-------------------------------------------------------------------------
"""

import json

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

def create_reverse_map(cipher_map):
    """
    Creates a lookup table where the keys are the symbols and the 
    values are the original letters.
    """
    reverse_map = {}
    all_subs = []
    for plaintext_char, substitutes in cipher_map.items():
        for sub in substitutes:
            reverse_map[sub] = plaintext_char.upper()
            all_subs.append(sub)

    # Sort by length descending to ensure "12" is checked before "1"
    all_subs.sort(key=len, reverse=True)
    return reverse_map, all_subs

def homophonic_decode(ciphertext, reverse_map, sorted_subs):
    """
    Decrypts the ciphertext by matching symbols to their original letters.
    """
    plaintext = []
    i = 0
    N = len(ciphertext)
    
    while i < N:
        found = False
        # Try to match the longest symbols first
        for sub in sorted_subs:
            sub_len = len(sub)
            if ciphertext[i : i + sub_len] == sub:
                plaintext.append(reverse_map[sub])
                i += sub_len
                found = True
                break
        
        if not found:
            # If no match, keep the character (like a comma or newline)
            plaintext.append(ciphertext[i])
            i += 1
            
    return "".join(plaintext)

# --- Main execution block ---
if __name__ == "__main__":
    # 1. Load and reverse the map
    mapping = load_cipher_map()
    
    if mapping:
        rev_map, subs_list = create_reverse_map(mapping)
        
        # 2. Get user input
        cipher_input = input("Enter the text to decode: ")
        
        # 3. Perform decoding
        decoded_text = homophonic_decode(cipher_input, rev_map, subs_list)
        
        # 4. Print results
        print("\n--- Decoded Plaintext ---")
        print(decoded_text)
        print("-------------------------\n")