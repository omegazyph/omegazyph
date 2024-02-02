#!/usr/bin/env python3

'''
Caesar cipher
by Wayne Stock
Created 2024-01-06
this will decode and encrypt a message with a key
'''

# Define the alphabet as a constant
ALPHABET = "abcdefghijklmnopqrstuvwxyz"

def encode():
    """
    Encodes a message using the Caesar cipher.
    """
    try:
        # Get the key from user input and convert it to an integer
        key = int(input("What is the Key: "))
    except ValueError:
        # Handle the case where the user enters a non-integer value for the key
        print("Invalid key. Please enter a valid integer.")
        return

    # Get the message to encode from user input
    incoming_message = input("\nWhat is the message I need to Encode?\n")
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
    print("\nHere is your coded message.\n" + outgoing_message)

# Call the function to execute the encoding process
encode()
