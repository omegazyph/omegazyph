######################################################################
# SecurePassGen
# Created by Wayne Stock (omegazyph)
# created on 2024-04-23
# This program uses Tkinter to create a password for the user.
#######################################################################

# Imports
import random
import string
import tkinter as tk
from tkinter import messagebox, simpledialog, Text, Toplevel, Button, Label, Entry

# Main App Class
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Secure Password Generator")  # Set the title of the window
        self.geometry('400x200')  # Set the initial size of the window
        self.configure(background="#f0f0f0")  # Set background color of the window

        # Create a Label widget with text
        self.main_label = Label(self,
                                text="Welcome to Secure Password Generator",  # Text displayed in the label
                                font=("Helvetica", 16),  # Font and size of the text
                                bg="#f0f0f0",  # Background color of the label
                                fg="#333333")  # Text color
        self.main_label.pack(pady=10)  # Pack the label into the window with some padding

        # Create an Entry widget to display the generated password
        self.output_entry = Entry(self, font=("Helvetica", 12), bg="white", fg="black", bd=0, highlightthickness=0)
        self.output_entry.pack(pady=10, padx=20, fill="x")

        # Create a Button widget
        self.gen_button = Button(self,
                                 text="Generate Password",  # Text displayed on the button
                                 command=self.generate_password)  # Function to be called when the button is clicked
        self.gen_button.pack(pady=10)  # Pack the button into the window with some padding

    # Function to generate password
    def generate_password(self, length=16, include_uppercase=True, include_lowercase=True, include_digits=True, include_symbols=True):
        characters = ''
        if include_uppercase:
            characters += string.ascii_uppercase
        if include_lowercase:
            characters += string.ascii_lowercase
        if include_digits:
            characters += string.digits
        if include_symbols:
            characters += string.punctuation

        if not characters:
            raise ValueError("At least one character type should be included")

        password = ''.join(random.choice(characters) for _ in range(length))  # Generate random password
        self.output_entry.delete(0, tk.END)  # Clear any previous password
        self.output_entry.insert(0, password)  # Display the generated password in the entry

# Entry Point
if __name__ == "__main__":
    window = App()  # Create an instance of the App class
    window.mainloop()  # Run the Tkinter event loop
