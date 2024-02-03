#!/usr/bin/env python3

'''
Caesar Cipher
by Wayne Stock
Created 2024-01-06
modified 2024-02-02
This program decodes a message from a file using the Caesar cipher and puts it in a new file.
'''
print("\nWelcome to Wayne\'s Decode Caesar Cipher!!!\n")
print("Warning please put the coded message in Decode.txt")

# to open a file with the meassage to read
with open('Cryptography/Caesar Cipher/Decode_code/Decode.txt') as file1:
    content = file1.read()


# Define the alphabet as a constant
ALPHABET = "abcdefghijklmnopqrstuvwxyz"

def decode():
    """
    Decodes a message using the Caesar cipher.
    """
    while True:
        try:
            # Get the key from user input and convert it to an integer
            key = int(input("Enter the Decryption key for decoding: "))
            
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
    incoming_message = content   #input("\nEnter the secret message to encode:\n")
    outgoing_message = ""
    

    # Iterate through each character in the input message
    for text in incoming_message:
        if text in ALPHABET:
            # If the character is in the alphabet, apply the Caesar cipher
            char = ALPHABET.find(text)
            outgoing_message += ALPHABET[(char + key) % 26]
        else:
            # If the character is not in the alphabet, leave it unchanged
            outgoing_message += text

    # Print the encoded message
    #print("\nYour coded message.\n" + outgoing_message)
    
    with open('Cryptography/Caesar Cipher/decode_code/plain_text', 'w') as file2:
        file2.write(outgoing_message)

# Call the function to execute the encoding process
decode()
