"""
Program: Password Generator
Author: Wayne Stock
Date: 2024-05-03
Description: This program generates a random password based on user input for length and repetition of characters.
"""

import random
from tkinter import messagebox, Tk, Label, Entry, Button, StringVar

# Define color code variables for UI
bd_color = 'black'
fg_color = 'white'

# Define a string containing letters, symbols, and numbers for password generation
character_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"

# Password generator function
def generate_password():
    try:
        # Get user input for repetition and length of the password
        repeat = int(repeat_entry.get())
        length = int(length_entry.get())
    except:
        # Show error message if input is not valid
        messagebox.showerror(message="Please key in the required inputs")
        return

    # Check if user allows repetition of characters
    if repeat == 1:
        password = random.sample(character_string, length)
    else:
        password = random.choices(character_string, k=length)

    # Convert the list of characters to a string
    password = ''.join(password)

    # Create a string variable to hold the password
    password_v = StringVar()
    password = "Created password: " + str(password)

    # Assign the password to the string variable
    password_v.set(password)

    # Create a read-only entry box to display the password
    password_label = Entry(password_gen, bd=0, bg="gray85", textvariable=password_v, state="readonly")
    password_label.place(x=10, y=140, height=50, width=320)

# Define the user interface
password_gen = Tk()
password_gen.geometry("350x200")
password_gen.title("Password Generator")

# Add title label for the app
title_label = Label(password_gen, text="Password Generator", font=('Ubuntu Mono', 12))
title_label.pack()

# Add label and entry for password length input
length_label = Label(password_gen, text="Enter length of password: ")
length_label.place(x=20, y=30)
length_entry = Entry(password_gen, width=3)
length_entry.place(x=190, y=30)

# Add label and entry for repetition input
repeat_label = Label(password_gen, text="Repetition? 1: no repetition, 2: otherwise: ")
repeat_label.place(x=20, y=60)
repeat_entry = Entry(password_gen, width=3)
repeat_entry.place(x=300, y=60)

# Add button to generate password
password_button = Button(password_gen, text="Generate Password", command=generate_password)
password_button.place(x=100, y=100)

# Start the Tkinter event loop
password_gen.mainloop()
