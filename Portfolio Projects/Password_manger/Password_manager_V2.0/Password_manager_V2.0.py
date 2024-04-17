from cryptography.fernet import Fernet

print("do not use | ")  # Print a warning message

def bcolor():
    pass

def banner():
    pass


# Function to generate and write a new key to a file
def write_key():
    """Generates a new encryption key and writes it to a file."""
    key = Fernet.generate_key()
    with open("key.key", 'wb') as key_file:
        key_file.write(key)
        print('Wrote a new key')

# Function to load the key from the file
def load_key():
    """Loads the encryption key from a file."""
    try:
        file = open("key.key", 'rb')
        key = file.read()
        file.close()
        return key 
    except FileNotFoundError:
        print("Key file not found")
        # Prompt user to create a new key if it doesn't exist
        choice = input("Would you like to create a key? (yes/no) <: ")
        if choice == "yes":
            write_key()
            print("You need to restart the program")
            quit()
        else:
            print("If you already have a key, put it in the current working directory")
            quit()

# Asking for the master password and loading the key
master_pwd = input("What is the master password? :> ")
key = load_key()
fer = Fernet(key)

# Function to create a password (not implemented)
def create_pwd():
    """Function to create a password (not implemented yet)."""
    pass

# Function to view existing passwords
def view():
    """Function to view existing passwords."""
    try:
        with open('passwords.txt', 'r') as f:
            for line in f.readlines():
                data = line.rstrip()
                user, passw = data.split("|")
                print("User:", user, "| Password:", fer.decrypt(passw.encode()).decode())
    except FileNotFoundError:
        # If password file doesn't exist, prompt user to create one
        choice = input("Can't find the password file. Would you like to create one? (yes/no) <:").lower()
        if choice == "yes":
            print("Please enter:")
            add()
        elif choice == "no":
            print("I need to create the file so I can store the passwords.")
            print("If you have a file already, please put the file in the working directory.")
            quit()
        else:
            print("Invalid selection")
            quit()

# Function to add a new password
def add():
    """Function to add a new password."""
    name = input("Account Name: ")
    pwd = input("Password: ")
    with open('passwords.txt', 'a') as f:
        f.write(name + '|' + fer.encrypt(pwd.encode()).decode() + "\n")

# Main loop for interacting with the user
while True:
    mode = input("Would you like to add a new password or view existing ones (view, add), press Q to Quit:> ").lower()
    if mode == "q":
        break

    if mode == "view":
        view()
    elif mode == "add":
        add()
    else:
        print("Invalid selection")
        continue
