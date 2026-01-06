########################################################
# Password Manager V 3.0
# created by Wayne Stock (omegazyph)
# created 2024-04-20
# This program is in Tkinter to help with managing passwords 
########################################################

# Imports
import tkinter as tk
from tkinter import messagebox, simpledialog, Text, Toplevel, Button, Label
from cryptography.fernet import Fernet

# Master Password (Change this to your desired master password)
MASTER_PASSWORD = "12345"

# Main Application Class
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Manager V3.0")
        self.geometry("400x300")
        self.configure(background="#f0f0f0")
        # Uncomment the line below to enable master password checking
        # self.check_master_password()

        # Widgets
        self.welcome_label = Label(self, text="Welcome to Password Manager V3.0", font=("Helvetica", 16), bg="#f0f0f0", fg="#333333")
        self.welcome_label.pack(pady=20)
        
        # Buttons for different functionalities
        self.write = Button(self, text="Create a Key", command=write.write_key)
        self.write.pack(side=tk.LEFT, padx=5)
        self.add = Button(self, text="Add a password", command=add.add)
        self.add.pack(side=tk.LEFT, padx=5)
        self.view = Button(self, text="View Passwords", command=self.view_passwords)
        self.view.pack(side=tk.LEFT, padx=5)

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
        passwords_window.title("Password List")
        text_widget = Text(passwords_window)
        text_widget.pack(fill=tk.BOTH, expand=True)
        View.display_passwords(text_widget)

# Write Key Functionality
class write:
    @staticmethod
    def write_key():
        try:
            result = messagebox.askquestion("Create Key", "Are you sure you want to create a new key?")
            if result == "yes":
                result_confirm = messagebox.askquestion("Confirmation", "Are you sure? This will replace your old key!")
                if result_confirm == "yes":
                    key = Fernet.generate_key()
                    with open("key.key", 'wb') as key_file:
                        key_file.write(key)
                    messagebox.showinfo("Key Created", "A new key has been successfully created.")
                else:
                    messagebox.showinfo("Cancelled", "Key creation has been cancelled.")
            else:
                messagebox.showinfo("Cancelled", "Key creation has been cancelled.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Load Key Functionality
class LoadKey:
    @staticmethod
    def load_key():
        try:
            with open("key.key", 'rb') as file:
                key = file.read()
                return key
        except FileNotFoundError:
            messagebox.showwarning("Warning", "Key file not found")
            choice = messagebox.askquestion("Create Key", "Would you like to create a key?")
            if choice == "yes":
                write.write_key()
            else:
                messagebox.showinfo("info", "If you already have a key, please put it in the current working directory")

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
                    file.write(site + '|' + username + ' | ' + fer.encrypt(pwd.encode()).decode() + "\n")
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
                for line in file.readlines():
                    data = line.rstrip()
                    site, user, password = data.split("|")
                    decrypted_password = fer.decrypt(password.encode()).decode()
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
