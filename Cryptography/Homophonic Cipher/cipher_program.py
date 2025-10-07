import json
import random

# -------------------- CORE FUNCTIONS --------------------

def load_cipher_map(filepath="cipher_map.json"):
    """Loads the substitution map from the JSON file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {filepath} was not found. Decoding/Encoding requires the key file.")
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
            # Randomly select one substitute from the list
            substitutes = cipher_map[char]
            ciphertext.append(random.choice(substitutes))
        else:
            # Keep spaces, punctuation, etc., as they are
            ciphertext.append(char)
            
    return "".join(ciphertext)

def create_reverse_map(cipher_map):
    """
    Creates a reverse map for decoding: {substitute: original_letter}
    It also returns substitutes sorted by length (longest first) for decoding logic.
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
    """Decrypts the message using the reverse substitution map."""
    plaintext = []
    i = 0
    N = len(ciphertext)
    
    while i < N:
        found = False
        # Try to match the LONGEST possible substitute at the current position (i)
        for sub in sorted_subs:
            sub_len = len(sub)
            
            # Check if the current slice of the ciphertext matches the substitute
            if ciphertext[i : i + sub_len] == sub:
                # Match found! Append original letter and advance the pointer
                plaintext.append(reverse_map[sub])
                i += sub_len
                found = True
                break
        
        if not found:
            # If no substitute is found, treat it as a non-ciphered character (space/punctuation)
            plaintext.append(ciphertext[i])
            i += 1

    return "".join(plaintext)

# -------------------- MAIN EXECUTION --------------------

if __name__ == "__main__":
    
    # 1. Load the cipher map
    cipher_map = load_cipher_map()
    if not cipher_map:
        exit()

    # 2. Prepare the decoding tools (The reverse map only needs to be created once)
    reverse_map, sorted_subs = create_reverse_map(cipher_map)

    print("\n--- Polyalphabetic Cipher Tool ---")
    
    while True:
        action = input("Do you want to (E)ncode or (D)ecode a message, or (Q)uit? ").strip().upper()

        if action == 'E':
            message = input("Enter the message to ENCODE: ")
            encrypted_text = encode_message(message, cipher_map)
            print(f"\nENCRYPTED MESSAGE: {encrypted_text}\n")
        
        elif action == 'D':
            message = input("Enter the message to DECODE: ")
            decrypted_text = decode_message(message, reverse_map, sorted_subs)
            print(f"\nDECRYPTED MESSAGE: {decrypted_text}\n")
            
        elif action == 'Q':
            print("Cipher tool closed. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter E, D, or Q.")