"""
-------------------------------------------------------------------------
PROJECT  : 256_bit Data
FILE     : 256_bit_data.py
AUTHOR   : omegazyph
DATE     : 12/24/2025
DESCRIPTION: Demonstrates symmetric encryption using the Fernet (AES-128) 
             standard, which uses 256-bit keys for secure data handling.
-------------------------------------------------------------------------
"""

from cryptography.fernet import Fernet

# 1. Generate a key
# This key must be kept secret. If lost, encrypted data cannot be recovered.
key = Fernet.generate_key()
f = Fernet(key)

print("\n")
print(f"The Key: {key.decode()}") # Decoded for cleaner console output
print("\n")

# 2. Define the payload
# The data must be in byte format (prefix with 'b')
password = b"mysecretpassword123"

# 3. Encrypt the data
# Fernet encryption provides strong 256-bit security and authenticity
encrypted_password = f.encrypt(password)

# 4. Output the results
print(f"Encrypted password: {encrypted_password.decode()}")
print("\n")

# 5. Decryption process
# We use the same Fernet instance (and key) to reverse the encryption
decrypted_password = f.decrypt(encrypted_password)

# Decode bytes back to a string for the final print
print(f"Decrypted password: {decrypted_password.decode()}")