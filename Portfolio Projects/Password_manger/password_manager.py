from cryptography.fernet import Fernet

print("do not use | ")

class PasswordManager:
    def __init__(self) -> None:
        # Asking for the master password and loading the key
        self.master_pwd = input("What is the master password? :> ")
        self.key = self.load_key()
        self.fer = Fernet(self.key)

    # Function to generate and write a new key to a file
    # don't call this function until you need a Key
    @staticmethod
    def write_key():
        key = Fernet.generate_key()
        with open("key.key", 'wb') as key_file:
            key_file.write(key)
        print('Wrote a new key')

    # Function to load the key from the file
    @staticmethod
    def load_key():
        with open("key.key", 'rb') as key_file:
            key = key_file.read()
        return key 

    # Function to create a password (not implemented)
    @staticmethod
    def create_pwd():
        pass

    # Function to view existing passwords
    @staticmethod
    def view():
        with open('passwords.txt', 'r') as f:
            for line in f:
                user, passw = line.strip().split("|")
                print("User:", user, "| Password:", PasswordManager.fer.decrypt(passw.encode()).decode())

    # Function to add a new password
    @staticmethod
    def add():
        name = input("Account Name :> ")
        pwd = input("Password :> ")

        with open('passwords.txt', 'a') as f:
            f.write(name + '|' + PasswordManager.fer.encrypt(pwd.encode()).decode() + "\n")

# Main loop for interacting with the user
while True:
    mode = input("Would you like to add a new password or view existing ones (view, add), press Q to Quit:> ").lower()
    if mode == "q":
        break

    if mode == "view":
        PasswordManager.view()
    elif mode == "add":
        PasswordManager.add()
    else:
        print("Invalid selection")
        continue
