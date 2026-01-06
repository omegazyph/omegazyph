########################################################
# Password Manager V 3.0
# created by Wayne Stock (omegazyph)
# created 2024-04-20
# This program is in Tkinter to help with managing passwords 
########################################################

# Imports
import tkinter as tk  # Import the Tkinter library
from tkinter import messagebox, simpledialog, Text, Toplevel, Button, Label  # Import specific components from Tkinter
from cryptography.fernet import Fernet  # Import Fernet from the cryptography library
import os  # Import os module for file operations

# Master Password (Change this to your desired master password)
MASTER_PASSWORD = "12345"  # Define the master password

# color Varables
bg_color = 'Black'
fg_color = 'White'
btn_color = 'Lightblue'
warning = 'Red'

# Main Application Class
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Manager V3.0")  # Set the title of the application window
        self.geometry("400x300")  # Set the size of the application window
        self.configure(bg=bg_color)  # Set the background color of the application window
        # leave in and uncommet when needed
        self.check_master_password() # check for the master password

        # Widgets
        self.welcome_label = Label(self, text="Welcome to Password Manager V3.0", font=("Helvetica", 16), bg=bg_color, fg=fg_color)
        self.welcome_label.pack(pady=20)  # Create a label widget and pack it into the window
        
        # Check if key file exists
        if not os.path.exists("key.key"):
            self.write_key_lable = Label(self, text="Your key is missing",bg=bg_color,fg=warning,font=("Helvetica", 16)).pack()
            self.write = Button(self, text="Create a Key", command=write.write_key, bg=btn_color)
            self.write.pack(pady=5)  # Create a button widget for creating a key
        
        self.add = Button(self, text="Add a password", command=add.add, bg=btn_color)
        self.add.pack(pady=5)  # Create a button widget for adding a password
        
        self.view = Button(self, text="View Passwords", command=self.view_passwords, bg=btn_color)
        self.view.pack(pady=5)  # Create a button widget for viewing passwords

        # need to work on
        self.view = Button(self, text="Change Master Password", command=self.view_passwords, bg=btn_color)
        self.view.pack(side=tk.RIGHT, anchor=tk.SE, padx=10, pady=10)  # Create a button widget for viewing passwords


    # Master Password Validation
    def check_master_password(self):
        while True:
            master_pwd = simpledialog.askstring("Master Password", "Enter the master password to access the program:")
            if master_pwd == MASTER_PASSWORD:
                break
            elif master_pwd is None:
                self.destroy()
                return
            else:
                messagebox.showerror("Incorrect Password", "Incorrect master password. Please try again.")

    # View Passwords Functionality
    def view_passwords(self):
        passwords_window = Toplevel(self)
        passwords_window.title("Password List")  # Create a new window for displaying passwords
        text_widget = Text(passwords_window)
        text_widget.pack(fill=tk.BOTH, expand=True)  # Create a text widget to display passwords
        View.display_passwords(text_widget)  # Call the display_passwords method from the View class

# Write Key Functionality
class write:
    @staticmethod
    def write_key():
        try:
            result = messagebox.askquestion("Create Key", "Are you sure you want to create a new key?")
            if result == "yes":
                result_confirm = messagebox.askquestion("Confirmation", "Are you sure? This will replace your old key!")
                if result_confirm == "yes":
                    key = Fernet.generate_key()  # Generate a new encryption key
                    with open("key.key", 'wb') as key_file:
                        key_file.write(key)  # Write the key to a file
                    messagebox.showinfo("Key Created", "A new key has been successfully created.")  # Display a message indicating successful key creation
                else:
                    messagebox.showinfo("Cancelled", "Key creation has been cancelled.")  # Display a message indicating key creation cancellation
            else:
                messagebox.showinfo("Cancelled", "Key creation has been cancelled.")  # Display a message indicating key creation cancellation
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")  # Display an error message if an exception occurs

# Load Key Functionality
class LoadKey:
    @staticmethod
    def load_key():
        try:
            with open("key.key", 'rb') as file:
                key = file.read()  # Read the key from the file
                return key  # Return the key
        except FileNotFoundError:
            messagebox.showwarning("Warning", "Key file not found")  # Display a warning message if the key file is not found
            choice = messagebox.askquestion("Create Key", "Would you like to create a key?")
            if choice == "yes":
                write.write_key()  # Call the write_key method if the user chooses to create a new key
            else:
                messagebox.showinfo("info", "If you already have a key, please put it in the current working directory")  # Display an information message

# Add Password Functionality
class add:
    @staticmethod
    def add():
        key = LoadKey.load_key()
        fer = Fernet(key)
        while True:
            site = simpledialog.askstring("Site Name", "Enter the name of the site you wish to add:")
            if site is None:
                return
            elif site == "":
                messagebox.showerror("Error", "Site can not be empty!")
                continue
            else:
                break
        while True:
            username = simpledialog.askstring("Username", "Enter the username of the site you wish to add:")
            if username is None:
                return
            if username == "":
                messagebox.showerror("Error", "Username can not be empty!")
                continue
            else:
                break
        while True:
            pwd = simpledialog.askstring("Password", "Enter the password of the site you wish to add:")
            if pwd is None:
                return
            if pwd == "":
                messagebox.showerror("Error", "Password can not be empty!")
                continue
            else:
                with open('passwords.txt', 'a') as file:
                    file.write(site + '|' + username + ' | ' + fer.encrypt(pwd.encode()).decode() + "\n")  # Encrypt the password and write it to a file
                    messagebox.showinfo("Saving", "Password is saved")
                break

# View Passwords Functionality
class View:
    @staticmethod
    def display_passwords(text_widget):
        key = LoadKey.load_key()
        fer = Fernet(key)
        try:
            with open('passwords.txt', 'r') as file:
                # Read passwords and store them in a list of tuples (site, user, password)
                passwords = []
                for line in file.readlines():
                    data = line.rstrip()
                    site, user, password = data.split("|")
                    decrypted_password = fer.decrypt(password.encode()).decode()
                    passwords.append((site, user, decrypted_password))
                
                # Sort passwords by site name
                sorted_passwords = sorted(passwords, key=lambda x: x[0])
                
                # Display sorted passwords
                for password in sorted_passwords:
                    site, user, decrypted_password = password
                    text_widget.insert(tk.END, f"Site: {site}\nUser: {user}\nPassword: {decrypted_password}\n\n")
        except FileNotFoundError:
            choice = messagebox.askquestion("Error", "Can't find the password file. Would you like to create one?")
            if choice == "yes":
                add.add()
            elif choice == "no":
                messagebox.showwarning("", "You need to create the file so You can store your passwords.")
                messagebox.showinfo("", "If you have a file already, please put the file in the working directory.")

# Entry Point
if __name__ == "__main__":
    app = Application()
    app.mainloop()
