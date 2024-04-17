from cryptography.fernet import Fernet

print("do not use | ")

# Function to generate and write a new key to a file
''' run if need a Key
def write_key():
    key = Fernet.generate_key()
    with open("key.key", 'wb') as key_file:
        key_file.write(key)
        print ('wrote a new new')
write_key()'''

# Function to load the key from the file
def load_key():
    file = open("key.key", 'rb')
    key = file.read()
    file.close()
    return key 

# Asking for the master password and loading the key
master_pwd = input("What is the master password? :> ")
key = load_key()
fer = Fernet(key)

# Function to create a password (not implemented)
def create_pwd():
    pass

# Function to view existing passwords
def view():
    with open('passwords.txt', 'r') as f:
        for line in f.readlines():
            data = line.rstrip()
            user, passw = data.split("|")
            print("User:",user, "| Password:", fer.decrypt(passw.encode()).decode())

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
        print("Invalid mode")
        continue
