'''
BruteForce Attack on Caesar Cipher
by Wayne Stock
Created 2024-01-06
modified 2024-02-03
this will run through the keys to decode the message
'''

# Define the alphabet as a constant
ALPHABET = "abcdefghijklmnopqrstuvwxyz"

# Get the message to be decoded from the user
message = input("What is the message you would like to Decode: ")
outgoing_message = ""  # Variable to store the decoded message
key = 0  # Initial key value

def bruteForce_Attack(message, key, outgoing_message):
    """
    Function to perform a brute-force attack on a Caesar Cipher.

    Args:
    - message (str): The message to be decoded.
    - key (int): The key used for decryption.
    - outgoing_message (str): Variable to store the decoded message.

    Returns:
    - str: The decrypted message.
    """
    for x in message:
        if x in ALPHABET:
            char = ALPHABET.find(x)
            outgoing_message += ALPHABET[(char + int(key)) % 26]
        else:
            outgoing_message += x

    return outgoing_message

# Iterate through all possible keys (0 to 25) and print the decrypted message for each key
for i in range(26):
    plain_text = bruteForce_Attack(message, i, outgoing_message)
    print("For key {}, decrypted text: {}".format(i, plain_text))
