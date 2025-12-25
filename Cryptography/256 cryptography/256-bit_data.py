from cryptography.fernet import Fernet

# 1. Generate a key (do this once and store it securely)
key = Fernet.generate_key()
f = Fernet(key)
print("\n")
print(f"The Key: {key}")
print("\n")

# 2. Define your password (must be bytes)
password = b"mysecretpassword123"

# 3. Encrypt the password 
encrypted_password = f.encrypt(password)


# 4. Print the encrypted password (this will be in bytes)
print(f"Encrypted password: {encrypted_password}")
print("\n")

# to decrypt later:
decrypted_password = f.decrypt(encrypted_password)
print(f"Decryped password: {decrypted_password.decode()}")
# Decode bytes back to a sting