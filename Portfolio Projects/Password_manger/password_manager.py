from cryptography.fernet import Fernet

print("do not use | ")

class Password_manager:

    # Function to generate and write a new key to a file
    # don't call this function until you need a Key
    def write_key():
        try:
            key = Fernet.generate_key()
            with open("key.key", 'wb') as key_file:
                key_file.write(key)
                print ('wrote a new Key')
        except Exception as e:
            print("Error: ", e )


    # Function to load the key from the file
    def load_key():
        file = open("key.key", 'rb')
        key = file.read()
        file.close()
        return key 

    

    # Function to create a password (not implemented)
    def create_pwd():
        pass

    # Function to view existing passwords
    def view():
        with open('passwords.txt', 'r') as f:
            for line in f.readlines():
                data = line.rstrip()
                user, passw = data.split("|")
                print("User:",user, "| Password:", Password_manager.fer.decrypt(passw.encode()).decode())

    # Function to add a new password
    def add():
        name = input("Account Name :> ")
        pwd = input("Password :> ")

        with open('passwords.txt', 'a') as f:
            f.write(name + '|' + Password_manager.fer.encrypt(pwd.encode()).decode() + "\n")

# Main loop for interacting with the user
while True:
    # Asking for the master password and loading the key
    master_pwd = input("What is the master password? :> ")
    if master_pwd == "hello":
        key = Password_manager.load_key()
        fer = Fernet(key)
    else:
        print("Wrong Password! try again")
        continue
        #optional
        #print("get the Fuck out")

    
    mode = input("Would you like to add a new password or view existing ones (view, add), press Q to Quit:> ").lower()
    if mode == "q":
        break

    if mode == "view":
        Password_manager.view()
    elif mode == "add":
        Password_manager.add()
    else:
        print("Invalid selection")
        continue
