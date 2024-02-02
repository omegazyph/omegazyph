#!/usr/bin/env python3


'''
Caesar cipher
by Wayne Stock
Created 2024-01-06
this will decode and encrypt a message with a key
'''

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def encode():
  
  
  # Key Validation
  try:
    key = int(input("What is the Key: "))
  except ValueError:
    print("Invalid key. Please enter a valid integer.")
    return

        
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
