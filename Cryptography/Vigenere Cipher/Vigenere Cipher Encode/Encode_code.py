#!/usr/bin/env python3

'''
Vigenere Cipher
Author: Wayne Stock
Created: 2024-02-03
This program encodes a file using Vigenere Cipher into another file.
'''

print("\nWarning: Make sure your file is in the directory!")

# ALPHABET is a constant representing the alphabet for encryption and decryption
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


def vigenere_decode(message, keyword):
    """
    Decrypt the message using the Vigenere Cipher.

    Args:
    - message (str): The message to be decoded.
    - keyword (str): The keyword used for decryption.

    Returns:
    - str: The decoded message.
    """
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
    @staticmethod
    def get_file_contents():
        """
        Prompt the user for the filename or file path and read the file contents.

        Returns:
        - str: The contents of the file.
        """
        while True:
            file_name = input("Enter the filename or file path: ")

            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    file_contents = file.read()

                print("Contents of the file:")
                print(file_contents)
                return file_contents

            except FileNotFoundError:
                print(f"File '{file_name}' not found.")

            except PermissionError:
                print(f"Permission error: Unable to read file '{file_name}'.")

            except Exception as e:
                print(f"An error occurred: {e}")


# Get file contents using the UserInput class
file_contents = UserInput.get_file_contents()

# Get user input for the keyword and use the file contents as the message
while True:
    vigenere_keyword = input("Enter your keyWord: ")
    # Validate that the keyword contains only valid characters
    if all(char.isalpha() and char.islower() for char in vigenere_keyword):
        break
    else:
        print("Invalid characters in the keyword. Please use only lowercase letters.")

if file_contents:
    # Display the decoded message
    print("Here is your Decoded message:\n" + vigenere_decode(file_contents, vigenere_keyword))
