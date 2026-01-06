#!/usr/bin/env python3
"""
==============================================================================
SCRIPT NAME:    secure_pass_gen.py
DESCRIPTION:    A Tkinter-based application that generates secure, random 
                passwords using strings of letters, digits, and symbols.
AUTHOR:         omegazyph
DATE CREATED:   2024-04-23
DATE UPDATED:   2026-01-05
VERSION:        2.1
==============================================================================
"""

# Imports
import random
import string
import tkinter as tk
from tkinter import messagebox, Label, Entry, Button

# Main App Class
class App(tk.Tk):
    """Main application class for the Secure Password Generator."""
    def __init__(self):
        super().__init__()
        self.title("Secure Password Generator")  # Set the title of the window
        self.geometry('400x250')  # Set the initial size of the window
        self.configure(background="#f0f0f0")  # Set background color of the window

        # Create a Label widget for the title
        self.main_label = Label(
            self,
            text="Secure Password Generator",
            font=("Helvetica", 16, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        self.main_label.pack(pady=10)

        # Create an Entry widget to display the generated password
        # We use a readonly state later to prevent manual typing in the box
        self.output_entry = Entry(
            self, 
            font=("Helvetica", 12), 
            bg="white", 
            fg="black", 
            bd=1, 
            relief="solid", 
            justify="center"
        )
        self.output_entry.pack(pady=10, padx=20, fill="x")

        # Create a Button widget to trigger generation
        self.gen_button = Button(
            self,
            text="Generate Password",
            font=("Helvetica", 10),
            command=self.generate_password,
            bg="#4CAF50",
            fg="white",
            width=20
        )
        self.gen_button.pack(pady=5)

        # Button to copy the generated password to the clipboard
        self.copy_button = Button(
            self,
            text="Copy to Clipboard",
            font=("Helvetica", 10),
            command=self.copy_to_clipboard,
            bg="#2196F3",
            fg="white",
            width=20
        )
        self.copy_button.pack(pady=5)

    def generate_password(self, length=16):
        """Logic to build a random string from various character sets."""
        # Define the possible characters
        characters = string.ascii_letters + string.digits + string.punctuation

        # Generate a random password of the specified length
        password = ''.join(random.choice(characters) for i in range(length))
        
        # Enable the entry to update the text, then disable it again
        self.output_entry.config(state='normal')
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, password)
        # Setting to readonly so the user doesn't accidentally change it
        self.output_entry.config(state='readonly')

    def copy_to_clipboard(self):
        """Retrieves the password from the entry and puts it on the system clipboard."""
        password = self.output_entry.get()
        if password:
            self.clipboard_clear()
            self.clipboard_append(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "Generate a password first!")

# Entry Point
if __name__ == "__main__":
    # Create an instance of the App class
    window = App()
    # Run the Tkinter event loop to keep the window open
    window.mainloop()