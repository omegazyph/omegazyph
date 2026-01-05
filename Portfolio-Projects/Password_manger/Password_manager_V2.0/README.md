# Simple Password Manager

This Python script serves as a simple password manager, allowing users to securely store and manage their passwords for different accounts.

## Features

- **Encryption**: Passwords are encrypted using the Fernet algorithm for security.
- **View Passwords**: Users can view their stored passwords.
- **Add Passwords**: Users can add new passwords for their accounts.

## Getting Started

1. **Dependencies**: Install the cryptography library using `pip install cryptography`.
2. **Generate Key**: Uncomment the `write_key()` function to generate an encryption key.
3. **Set Master Password**: Run the script and set a master password.
4. **Usage**: View, add, or quit the program using the prompts in the terminal.

## Usage

- **View Passwords**: Choose the "view" option to view existing passwords. Passwords are decrypted and displayed.
- **Add Passwords**: Choose the "add" option to add a new password. Enter the account name and password when prompted.
- **Quit**: Press "Q" to quit the program.

## File Structure

- `password_manager.py`: Main script for password management.
- `key.key`: File containing the encryption key.
- `passwords.txt`: Text file storing encrypted account names and passwords.

## Security Note

- Ensure the `key.key` file is kept secure as it's essential for decrypting passwords.
- Avoid using special characters like '|' in account names or passwords.

## License

This project is licensed under the [MIT License](LICENSE).
