#!/usr/bin/env python3
"""
==============================================================================
SCRIPT NAME:    password_manager_v3.py
DESCRIPTION:    A Tkinter-based Password Manager for managing and encrypting 
                passwords using the cryptography library.
AUTHOR:         omegazyph
DATE CREATED:   2024-04-20
DATE UPDATED:   2026-01-05
VERSION:        3.1
==============================================================================
"""

import tkinter as tk
from tkinter import messagebox, simpledialog, Text, Toplevel, Button, Label
from cryptography.fernet import Fernet
import os

# Master Password for program access
MASTER_PASSWORD = "12345"

# Color Variables for the UI
bg_color = 'Black'
fg_color = 'White'
btn_color = 'Lightblue'
warning = 'Red'

class Application(tk.Tk):
    """Main window class for the Password Manager GUI."""
    def __init__(self):
        super().__init__()
        self.title("Password Manager V3.1")
        self.geometry("400x350")
        self.configure(bg=bg_color)
        
        # Security check: Asks for master password before showing the main menu
        self.check_master_password()

        self.welcome_label = Label(self, text="Password Manager V3.1", 
                                   font=("Helvetica", 16), bg=bg_color, fg=fg_color)
        self.welcome_label.pack(pady=20)
        
        # Check for key.key and provide a button if it is missing
        if not os.path.exists("key.key"):
            # Fixed: Put label on its own line
            self.missing_label = Label(self, text="Your key is missing", bg=bg_color, 
                                       fg=warning, font=("Helvetica", 12))
            self.missing_label.pack()
            
            self.write_btn = Button(self, text="Create a Key", 
                                    command=write.write_key, bg=btn_color)
            self.write_btn.pack(pady=5)
        
        self.add_btn = Button(self, text="Add a password", 
                              command=add.add, bg=btn_color, width=20)
        self.add_btn.pack(pady=5)
        
        self.view_btn = Button(self, text="View Passwords", 
                               command=self.view_passwords, bg=btn_color, width=20)
        self.view_btn.pack(pady=5)

    def check_master_password(self):
        """Validates the user against the MASTER_PASSWORD constant."""
        while True:
            master_pwd = simpledialog.askstring("Master Password", 
                                                "Enter password to access:", show='*')
            if master_pwd == MASTER_PASSWORD:
                break
            elif master_pwd is None:
                self.destroy()
                exit()
            else:
                messagebox.showerror("Incorrect Password", "Try again.")

    def view_passwords(self):
        """Creates a new window to display the decrypted list of passwords."""
        passwords_window = Toplevel(self)
        passwords_window.title("Password List")
        passwords_window.geometry("400x400")
        
        text_widget = Text(passwords_window)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Call the View class to fill the text widget
        View.display_passwords(text_widget)

class write:
    """Handles creating a new encryption key."""
    @staticmethod
    def write_key():
        # Fixed: Logic moved to new lines instead of staying after the colon
        if messagebox.askquestion("Create Key", "Replace old key? Are you sure?") == "yes":
            key = Fernet.generate_key()
            with open("key.key", 'wb') as key_file:
                key_file.write(key)
            messagebox.showinfo("Success", "Key created.")

class LoadKey:
    """Handles reading the encryption key from the file."""
    @staticmethod
    def load_key():
        try:
            with open("key.key", 'rb') as file:
                return file.read()
        except FileNotFoundError:
            return None

class add:
    """Handles adding and encrypting new site credentials."""
    @staticmethod
    def add():
        key = LoadKey.load_key()
        if not key:
            messagebox.showerror("Error", "No key found!")
            return
            
        fer = Fernet(key)
        site = simpledialog.askstring("Site", "Enter Site Name:")
        user = simpledialog.askstring("Username", "Enter Username:")
        pwd = simpledialog.askstring("Password", "Enter Password:", show='*')

        if site and user and pwd:
            encrypted_pwd = fer.encrypt(pwd.encode()).decode()
            with open('passwords.txt', 'a') as file:
                file.write(f"{site}|{user}|{encrypted_pwd}\n")
            messagebox.showinfo("Saved", "Password has been stored.")

class View:
    """Handles decryption and display logic."""
    @staticmethod
    def display_passwords(text_widget):
        key = LoadKey.load_key()
        if not key:
            # Fixed: Added a check for missing key in view
            return
        
        fer = Fernet(key)
        try:
            with open('passwords.txt', 'r') as file:
                lines = file.readlines()
                lines.sort()
                
                for line in lines:
                    data = line.rstrip()
                    if "|" in data:
                        # Fixed: Logic moved to new lines to satisfy PEP 8
                        site, user, password = data.split("|")
                        decrypted = fer.decrypt(password.encode()).decode()
                        text_widget.insert(tk.END, f"Site: {site}\nUser: {user}\nPass: {decrypted}\n")
                        text_widget.insert(tk.END, "-"*20 + "\n")
        except FileNotFoundError:
            messagebox.showinfo("Empty", "No password file found.")

# Start the application
if __name__ == "__main__":
    app = Application()
    app.mainloop()