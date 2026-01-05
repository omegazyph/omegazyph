# Random Password Generator

This Python script generates random passwords with various customizable options.

## Usage

To use the password generator, simply call the `generate_password` function with desired parameters:

```python
import random
import string

def generate_password(length=12, include_uppercase=True, include_lowercase=True, include_digits=True, include_symbols=True):
    """
    Generate a random password.

    Args:
    - length (int): Length of the password (default is 12)
    - include_uppercase (bool): Whether to include uppercase letters (default is True)
    - include_lowercase (bool): Whether to include lowercase letters (default is True)
    - include_digits (bool): Whether to include digits (default is True)
    - include_symbols (bool): Whether to include symbols (default is True)

    Returns:
    - str: Generated password
    """
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
