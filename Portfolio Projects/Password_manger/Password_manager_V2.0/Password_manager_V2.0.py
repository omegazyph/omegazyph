from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self):
        self.key_file = "key.key"
        self.passwords_file = "passwords.txt"
        self.fer = None

    def write_key(self):
        """Generate and write a new key to a file."""
        key = Fernet.generate_key()
        with open(self.key_file, 'wb') as key_file:
            key_file.write(key)
        print("Generated and wrote a new key")

    def load_key(self):
        """Load the encryption key from the file."""
        try:
            with open(self.key_file, 'rb') as key_file:
                key = key_file.read()
            return key
        except FileNotFoundError:
            print("Key file not found.")
            return None
        except Exception as e:
            print("Error loading key:", e)
            return None

    def initialize_fernet(self):
        """Initialize the Fernet instance with the loaded key."""
        key = self.load_key()
        if key:
            self.fer = Fernet(key)
            return True
        return False

    def view_passwords(self):
        """View existing passwords."""
        try:
            with open(self.passwords_file, 'r') as f:
                for line in f:
                    user, passw = line.strip().split("|")
                    print("User:", user, "| Password:", self.fer.decrypt(passw.encode()).decode())
        except FileNotFoundError:
            print("Passwords file not found.")
        except Exception as e:
            print("Error viewing passwords:", e)

    def add_password(self):
        """Add a new password."""
        name = input("Account Name: ")
        pwd = input("Password: ")
        encrypted_pwd = self.fer.encrypt(pwd.encode()).decode()
        with open(self.passwords_file, 'a') as f:
            f.write(name + '|' + encrypted_pwd + "\n")
        print("Password added successfully.")

def main():
    # Initialize PasswordManager instance
    password_manager = PasswordManager()
    password_manager.initialize_fernet()

    # Main loop for interacting with the user
    while True:
        mode = input("Would you like to add a new password or view existing ones (view, add), press Q to Quit: ").lower()
        if mode == "q":
            break

        if mode == "view":
            password_manager.view_passwords()
        elif mode == "add":
            password_manager.add_password()
        else:
            print("Invalid selection")

if __name__ == "__main__":
    main()
