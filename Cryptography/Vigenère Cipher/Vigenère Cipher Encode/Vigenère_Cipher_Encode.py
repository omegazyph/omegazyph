#!/usr/bin/env python3



ALPLABET = 'abcdefghijklmnopqrstuvwxyz'

def vigenere_decode(message, keyword):
  keyword_phrase = ""
  keyword_index = 0

  for character in message:
    if keyword_index >= len(keyword):
      keyword_index = 0
    if character in ALPLABET:
      keyword_phrase += keyword[keyword_index]
      keyword_index += 1
    else:
      keyword_phrase += character

  encoded_message = ""

  for i in range(len(message)):
    if message[i] in ALPLABET:
      old_character_index = ALPLABET.find(message[i])
      offset_index = ALPLABET.find(keyword_phrase[i])
      new_character = ALPLABET[(old_character_index - offset_index) % 26]
      encoded_message += new_character
    else:
      encoded_message += message[i]
    
  return encoded_message

vigenere_message = input("Enter your Message:\n")
vigenere_keyword = input("Enter your keyWord:\n")

print("Here is your Encoded message:\n" + vigenere_decode(vigenere_message, vigenere_keyword))