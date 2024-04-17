from cryptography.fernet import Fernet

print("do not use | ")

# Function to generate and write a new key to a file

def write_key():
    key = Fernet.generate_key()
    with open("key.key", 'wb') as key_file:
        key_file.write(key)
        print ('wrote a new key')


# Function to load the key from the file
def load_key():
    try:
        file = open("key.key", 'rb')
        key = file.read()
        file.close()
        return key 
    
    except FileNotFoundError:
        print("key file not found")
        choice = input("would you like to create a key? (yes/no) <: ")
        if choice == "yes":
            write_key()
            print(" you need to retart the program ")
            quit()
        else:
            print("if you already have a key, put it in the current working dirtory")
            quit()


# Asking for the master password and loading the key
master_pwd = input("What is the master password? :> ")
key = load_key()
fer = Fernet(key)

# Function to create a password (not implemented)
def create_pwd():
    pass

# Function to view existing passwords
def view():
    try:
        with open('passwords.txt', 'r') as f:
            for line in f.readlines():
                data = line.rstrip()
                user, passw = data.split("|")
                print("User:",user, "| Password:", fer.decrypt(passw.encode()).decode())
    except FileNotFoundError:
        choice = input("can't find the password file, would you like to start one? (yes/no) <:").lower()
        if choice == "yes":
            print("Please enter:\n")
            add()
        elif choice == "no":
            print("I need to create the file so i can store the passwords")
            print("If you have a file already please put the file in the working dirertry")
            quit()
        else:
            print("Invaild Entery")

# Function to add a new password
def add():
    name = input("Account Name :> ")
    pwd = input("Password :> ")

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
