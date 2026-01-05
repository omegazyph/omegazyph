import random
import string

def generate_password(length=12, include_uppercase=True, include_lowercase=True, include_digits=True, include_symbols=True):
    characters = ''
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_digits:
        characters += string.digits
    if include_symbols:
        characters += string.punctuation

    if not characters:
        raise ValueError("At least one character type should be included")

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Example usage
password = generate_password(length=16, include_uppercase=True, include_lowercase=True, include_digits=True, include_symbols=True)
print("Generated Password:", password)
