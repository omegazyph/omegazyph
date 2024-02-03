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

# Get user input for the message and keyword
vigenere_message = input("Enter your Message:\n")
vigenere_keyword = input("Enter your keyWord:\n")

# Display the decoded message
print("Here is your Decoded message:\n" + vigenere_decode(vigenere_message, vigenere_keyword))
