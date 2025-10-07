import json
import random
import os # Imported for potential future use or better error checking, but not strictly required for this core logic

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

def write_message_to_file(filepath, message):
    """Writes the given message string to a specified file."""
    try:
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
        print(f"Error: The key file '{filepath}' was not found. Decoding/Encoding requires the key file.")
        return None

def encode_message(plaintext, cipher_map):
    """Encrypts the message using the polyalphabetic substitution map."""
    if not cipher_map or not plaintext:
        return ""

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
    Creates a reverse map for decoding: {substitute: original_letter}.
    Returns the map and a list of substitutes sorted by length (longest first).
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

    # 2. Prepare the decoding tools
    reverse_map, sorted_subs = create_reverse_map(cipher_map)

    print("\n--- File-Based Polyalphabetic Cipher Tool ---")
    
    while True:
        action = input("Do you want to (E)ncode or (D)ecode a file, or (Q)uit? ").strip().upper()

        if action == 'E':
            print("\n--- ENCODE ---")
            input_file = input("Enter the input text file name (e.g., plaintext.txt): ")
            output_file = input("Enter the output file name for the ciphertext (e.g., ciphertext.txt): ")
            
            # Read, Encode, Write
            plaintext = read_message_from_file(input_file)
            if plaintext is not None:
                encrypted_text = encode_message(plaintext, cipher_map)
                write_message_to_file(output_file, encrypted_text)
        
        elif action == 'D':
            print("\n--- DECODE ---")
            input_file = input("Enter the input ciphertext file name (e.g., ciphertext.txt): ")
            output_file = input("Enter the output file name for the decrypted text (e.g., decrypted.txt): ")
            
            # Read, Decode, Write
            ciphertext = read_message_from_file(input_file)
            if ciphertext is not None:
                decrypted_text = decode_message(ciphertext, reverse_map, sorted_subs)
                write_message_to_file(output_file, decrypted_text)
            
        elif action == 'Q':
            print("\nCipher tool closed. Goodbye! 👋")
            break
            
        else:
            print("Invalid choice. Please enter E, D, or Q.")