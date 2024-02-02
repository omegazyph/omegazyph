#!/bin/env python 3

'''
Caesar cipher
by Wayne Stock
Created 2024-01-06
this will decode and encrypt a message with a key
'''

alphabet = "abcdefghijklmnopqrstuvwxyz"

def encode():
  
  key = input("What is the Key: ")
  incoming_message = input("\nWhat is the message I need to Encode?\n")
  outgoing_message = ""

  for text in incoming_message:
      if text in alphabet:
          char = alphabet.find(text)
          outgoing_message += alphabet[(char - int(key)) % 26]
      else:
          outgoing_message += text

  print("\nHere is your coded message.\n" + outgoing_message)

# Call the function
encode()
