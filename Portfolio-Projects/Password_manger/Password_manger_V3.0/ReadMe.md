# Password Manager V3.0

Password Manager V3.0 is a simple password management tool built using Tkinter and cryptography in Python. It allows users to securely store their passwords for different websites or services.

## Features

- **Master Password:** Users need to set a master password to access the program.
- **Key Management:** The program generates and manages encryption keys to securely encrypt and decrypt passwords.
- **Add Passwords:** Users can add passwords for different sites along with their usernames.
- **View Passwords:** Users can view the list of stored passwords.

## Requirements

- Python 3.x
- Tkinter (usually included in Python installations)
- cryptography library (install using `pip install cryptography`)

## Installation

1. Clone the repository:

    ```
    git clone https://github.com/yourusername/password-manager.git
    ```

2. Navigate to the project directory:

    ```
    cd password-manager
    ```

3. Install the required dependencies:

    ```
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:

    ```
    python password_manager.py
    ```

2. Upon running, you will be prompted to enter the master password. Enter the master password to access the password manager.

3. Once authenticated, you can choose from the following options:
   - **Create a Key:** Generate a new encryption key.
   - **Add a password:** Add a new password for a site/service.
   - **View Passwords:** View the list of stored passwords.

4. To exit the application, simply close the main window.

## Important Note

- Ensure to remember the master password as it is required to access the password manager.
- Keep the `key.key` file generated securely as it is used for encryption and decryption.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is licensed under the [MIT License](LICENSE).
