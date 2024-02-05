#!/usr/bin/env python3
'''
Vigenere Cipher Decode
by wayne stock
created 2024-02-05
this will decode the vigenere code from one file to another
'''

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

class main:

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
  vigenere_message = input("Enter your message to Decode:\n")
  vigenere_keyword = input("Enter the KeyWord:\n")

print("Here is the message:\n" + vigenere_decode(vigenere_message, vigenere_keyword))