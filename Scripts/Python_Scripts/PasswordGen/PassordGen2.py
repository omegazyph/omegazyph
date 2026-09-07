########################################################################################
# Date: 2026-09-07
# Script name: PasswordGen2.py
# Author: Wayne Stock
# Updated: 2026-09-07
# Discrption: 
#   This is a password Generator that shows it is better to us import Setcert not random
########################################################################################

# Do not use
'''
import random
import string

password = "".join(
    random.choices(
        string.ascii_letters, k=12
    )
)
print(password)

#the above is really not random it just looks like it 
# the attcker can product the seed
#############################################
'''

# use this: 
import secrets
import string

password = "".join(
    secrets.choice(string.ascii_letters)
    for _ in range(12)
)
print(password)
print(secrets.token_hex(16))

