#!/usr/bin/env python3

'''
Caesar Cipher
by Wayne Stock
Created 2024-01-06
modified 2024-02-02
This program encodes a message using the Caesar cipher.
'''
print("\nWelcome to Wayne\'s Caesar Cipher!!!\n")

# Define the alphabet as a constant
ALPHABET = "abcdefghijklmnopqrstuvwxyz"

def encode():
    """
    Encodes a message using the Caesar cipher.
    """
    while True:
        try:
            # Get the key from user input and convert it to an integer
            key = int(input("Enter the encryption key for encoding: "))
            
            # Check if the key is within a reasonable range (1 to 25)
            if 1 <= key <= 25:
                # Valid key, break out of the loop and proceed with encoding
                break
            else:
                print("Invalid key. Please enter an integer between 1 and 25.")

        except ValueError:
            # Handle the case where the user enters a non-integer value for the key
            print("Invalid key. Please enter a valid integer.")

    # Get the message to encode from user input
    incoming_message = input("\nEnter the secret message to encode:\n")
    outgoing_message = ""

    # Iterate through each character in the input message
    for text in incoming_message:
        if text in ALPHABET:
            # If the character is in the alphabet, apply the Caesar cipher
            char = ALPHABET.find(text)
            outgoing_message += ALPHABET[(char - key) % 26]
        else:
            # If the character is not in the alphabet, leave it unchanged
            outgoing_message += text

    # Print the encoded message
    print("\nYour coded message.\n" + outgoing_message)

# Call the function to execute the encoding process
encode()
