#!/usr/bin/env python3
'''
Vigenere Cipher Decode
by wayne stock
created 2024-02-05
this will decode the vigenere code from one file to another
'''


ALPHABET = "abcdefghijklmnopqrstuvwxyz"

class Main:

  def vigenere_decode(message, keyword):
    keyword_phrase = ""
    keyword_index = 0

    for character in message:
      if keyword_index >= len(keyword):
        keyword_index = 0
      if character in ALPHABET:
        keyword_phrase += keyword[keyword_index]
        keyword_index += 1
      else:
        keyword_phrase += character

    decoded_message = ""

    for i in range(len(message)):
      if message[i] in ALPHABET:
        old_character_index = ALPHABET.find(message[i])
        offset_index = ALPHABET.find(keyword_phrase[i])
        new_character = ALPHABET[(old_character_index + offset_index) % 26]
        decoded_message += new_character
      else:
        decoded_message += message[i]
    
    return decoded_message



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


class Key:
  while True:
    vigenere_keyword = input("Enter your keyWord: ")
    # Validate that the keyword contains only valid characters
    if all(char.isalpha() and char.islower() for char in vigenere_keyword):
        break
    else:
        print("Invalid characters in the keyword. Please use only lowercase letters.")



  #vigenere_message = input("Enter your message to Decode:\n")
  #vigenere_keyword = input("Enter the KeyWord:\n")
        
class Write_file:
   if file_contents:
    '''
    # Display the decoded message
    print("Here is your Decoded message:\n" + vigenere_decode(file_contents, vigenere_keyword))
    '''
   # Get user input for the file name
    user_input = input("Enter the filename or press Enter for the default name: ")

    # Check if the user provided a file name
    if user_input:
        file_name = user_input
    else:
        # Use a default name if no input is provided
        file_name = "default_filename.txt"

    # Now you can use the 'file_name' variable in your code
    print(f"Using file name: {file_name}")

    # Open the file in write mode ('w')
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(Main.vigenere_decode(file_contents, Key.vigenere_keyword))
