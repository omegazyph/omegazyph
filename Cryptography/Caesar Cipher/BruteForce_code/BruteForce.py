'''
BruteForce Attack on Caesar Ciipher
by Wayne Stock
Created 2024-01-06
this will run though the keys to decode the message
'''

alph = "abcdefghijklmnopqrstuvwxyz"
message = input("What is the message you like to Decode: ")
outgoing_message = ""
key = 0




def bruteForce_Attack(message,key,outgoing_message):
    for x in message:
        if x in alph:
            char = alph.find(x)
            outgoing_message += alph[(char + int(key)) % 26]
        else:
            outgoing_message += x
            
    return outgoing_message
        

for i in range(0,26):
    plain_text = bruteForce_Attack(message,i,outgoing_message)
    print("For key {}, decrypted text: {}".format(i, plain_text))