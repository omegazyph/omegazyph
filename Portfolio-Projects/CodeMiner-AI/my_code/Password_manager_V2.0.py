from cryptography.fernet import Fernet

# Function to set text color for terminal output
def bcolor(color):
    colors = {
        'green': '\033[92m',
        'red': '\033[91m',
        'yellow': '\033[93m',
        'white': '\033[0m',
        'blue': '\033[94m'
    }
    return colors.get(color.lower(), '')

# Example usage of color function
green_code = bcolor('green')
red_code = bcolor('red')
yellow_code = bcolor('yellow')
white_code = bcolor('white')
blue_code = bcolor('blue')

# Function to display banner
def banner():
    print(blue_code + """
    Your banner here
    """)

# Printing banner
banner()

# Function to generate and write a new key to a file
def write_key():
    """Generates a new encryption key and writes it to a file."""
    key = Fernet.generate_key()
    with open("key.key", 'wb') as key_file:
        key_file.write(key)
        print(green_code + 'Wrote a new key')

# Function to load the key from the file
def load_key():
    """Loads the encryption key from a file."""
    try:
        file = open("key.key", 'rb')
        key = file.read()
        file.close()
        return key 
    except FileNotFoundError:
        print(yellow_code + "Key file not found")
        # Prompt user to create a new key if it doesn't exist
        choice = input(green_code + "Would you like to create a key? (yes/no) <: ")
        if choice == "yes":
            write_key()
            print(yellow_code + "You need to restart the program")
            quit()
        else:
            print(yellow_code + "If you already have a key, put it in the current working directory")
            quit()

# Asking for the master password and loading the key
count = 0

while count < 3:
    master_pwd = input(green_code + "What is the master password? :> ")
    if master_pwd =="hello":  # Replace "hello" with your actual master password
        key = load_key()
        fer = Fernet(key)
        break
    else:
        print(red_code + "Wrong password")
        count += 1  
if count == 3:
    print(yellow_code + "GoodBye")
    quit() 

# Function to view existing passwords
def view():
    """Function to view existing passwords."""
    try:
        with open('passwords.txt', 'r') as f:
            for line in f.readlines():
                data = line.rstrip()
                user, passw = data.split("|")
                print(yellow_code + "User:", user, "| Password:", fer.decrypt(passw.encode()).decode())
    except FileNotFoundError:
        # If password file doesn't exist, prompt user to create one
        choice = input(yellow_code + "Can't find the password file. Would you like to create one? (yes/no) <:").lower()
        if choice == "yes":
            print(green_code + "Please enter:")
            add()
        elif choice == "no":
            print(red_code + "I need to create the file so I can store the passwords.")
            print("If you have a file already, please put the file in the working directory.")
            quit()
        else:
            print(red_code + "Invalid selection")
            quit()

# Function to add a new password
def add():
    """Function to add a new password."""
    name = input(white_code + "Account Name: ")
    if '|' in name:
        print(red_code + "Please do not use '|' character in the account name.")
        return   
    pwd = input(white_code + "Password: ")
    if '|' in pwd:
        print(red_code + "Please do not use '|' character in the account name.")
        return
    with open('passwords.txt', 'a') as f:
        f.write(name + '|' + fer.encrypt(pwd.encode()).decode() + "\n")

# Main loop for interacting with the user
while True:
    mode = input(green_code + "Would you like to add a new password or view existing ones (view, add), press Q to Quit:> ").lower()
    if mode == "q":
        break

    if mode == "view":
        view()
    elif mode == "add":
        add()
    else:
        print(red_code + "Invalid selection")
        continue
