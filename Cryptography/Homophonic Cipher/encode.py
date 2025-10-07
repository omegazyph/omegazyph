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
    - Selects a random symbol for each letter.
    - Keeps non-alphabetic characters (like spaces) as is.
    """
    if not cipher_map:
        return "Encoding failed: Cipher map not loaded."

    ciphertext = []
    
    for char in plaintext:
        # Convert character to uppercase for dictionary lookup (as planned)
        upper_char = char.upper()
        
        if upper_char in cipher_map:
            # Randomly select one substitute from the list for the letter
            substitute = random.choice(cipher_map[upper_char])
            ciphertext.append(substitute)
        else:
            # Keep the character as is (for spaces, punctuation, numbers)
            ciphertext.append(char)
            
    return "".join(ciphertext)

# --- Main execution block ---
if __name__ == "__main__":
    # 1. Load the map
    cipher_map = load_cipher_map()
    
    if cipher_map:
        # 2. Get user input
        plaintext = input("Enter the text to encode: ")
        
        # 3. Perform encoding
        encoded_text = homophonic_encode(plaintext, cipher_map)
        
        # 4. Print results
        print("\n--- Ciphertext ---")
        print(encoded_text)
        print("------------------\n")