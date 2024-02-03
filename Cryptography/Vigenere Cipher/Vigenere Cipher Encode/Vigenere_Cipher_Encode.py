#!/usr/bin/env python3

'''
Vigenere Cipher
author Wayne Stock
created 2024-02-03
this program will in encode a file using Vigenere Cipher
'''

# ALPHABET is a constant representing the alphabet for encryption and decryption
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


def vigenere_decode(message, keyword):
    keyword_phrase = ""
    keyword_index = 0

    # Build the keyword phrase based on the message and the given keyword
    for character in message:
        if keyword_index >= len(keyword):
            keyword_index = 0
        if character in ALPHABET:
            keyword_phrase += keyword[keyword_index]
            keyword_index += 1
        else:
            keyword_phrase += character

    encoded_message = ""
    # Decrypt the message using the Vigenere Cipher
    for i in range(len(message)):
        if message[i] in ALPHABET:
            old_character_index = ALPHABET.find(message[i])
            offset_index = ALPHABET.find(keyword_phrase[i])
            new_character = ALPHABET[(old_character_index - offset_index) % 26]
            encoded_message += new_character
        else:
            encoded_message += message[i]

    return encoded_message


class UserInput:
    # Get user input for the message and keyword
    @staticmethod
    def get_file_contents():
        # Prompt the user for the file name
        file_name = input("Enter the file name: ")

        try:
            # Open the file in read mode
            with open(file_name, 'r') as file:
                # Read the contents of the file
                file_contents = file.read()

            # Do something with the file contents (e.g., print them)
            print("Contents of the file:")
            print(file_contents)
            return file_contents

        except FileNotFoundError:
            print(f"File '{file_name}' not found.")
            return None

        except Exception as e:
            print(f"An error occurred: {e}")
            return None


# Get user input for the keyword and use the file contents as the message
vigenere_keyword = input("Enter your keyWord:\n")

# Get file contents using the UserInput class
file_contents = UserInput.get_file_contents()

if file_contents:
    # Display the decoded message
    print("Here is your Decoded message:\n" + vigenere_decode(file_contents, vigenere_keyword))
