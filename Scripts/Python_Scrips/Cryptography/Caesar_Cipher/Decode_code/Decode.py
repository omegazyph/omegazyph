"""
Date: 2026-01-29
Script Name: decode_logic.py
Author: omegazyph
Updated: 2026-01-29
Description: This program decodes a message from a file using the Caesar cipher 
and saves the output to a new file. It uses pathlib for robust path management on Windows 11.
"""

import pathlib

def decode_message():
    """
    Decodes a message using the Caesar cipher and handles file I/O.
    """
    # Define the alphabet as a constant
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    
    # Use pathlib to find the directory where this script is saved
    # This prevents 'File Not Found' errors in VSCode
    current_directory = pathlib.Path(__file__).parent.resolve()
    
    # Define the input and output file paths relative to the script location
    input_file_path = current_directory / "Decode.txt"
    output_file_path = current_directory / "plain_text.txt"

    print("\nWelcome to Wayne's Decode Caesar Cipher!!!\n")

    # Check if the input file exists before trying to open it
    if not input_file_path.exists():
        print(f"Error: The file {input_file_path.name} was not found in the folder.")
        print(f"Expected path: {input_file_path}")
        return

    # Open the file with the message to read
    with open(input_file_path, "r") as file_input:
        content = file_input.read().lower()

    while True:
        try:
            # Get the key from user input and convert it to an integer
            key = int(input("Enter the Decryption key for decoding (1-25): "))
            
            # Check if the key is within the valid range
            if 1 <= key <= 25:
                break
            else:
                print("Invalid key. Please enter an integer between 1 and 25.")
        except ValueError:
            print("Invalid key. Please enter a valid integer.")

    outgoing_message = ""

    # Iterate through each character in the input message
    for character in content:
        if character in ALPHABET:
            # Find the current position and apply the shift
            # We subtract the key for decoding, or add if the key was provided as a negative
            index = ALPHABET.find(character)
            # Standard Caesar decode logic: (index - key) % 26
            new_index = (index - key) % 26
            outgoing_message += ALPHABET[new_index]
        else:
            # If the character is not in the alphabet (space, punctuation), leave it unchanged
            outgoing_message += character

    # Write the decoded message to the output file
    with open(output_file_path, "w") as file_output:
        file_output.write(outgoing_message)
        
    print(f"\nSuccess! The decoded message has been saved to: {output_file_path.name}")

# Execute the function
if __name__ == "__main__":
    decode_message()