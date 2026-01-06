import tkinter as tk
from tkinter import messagebox

# Create main window
window = tk.Tk()
window.title("Message Box Example")

# Function to show an info message box
def show_info_message():
    messagebox.showinfo("Info", "This is an information message.")

# Function to show a warning message box
def show_warning_message():
    messagebox.showwarning("Warning", "This is a warning message.")

# Function to show an error message box
def show_error_message():
    messagebox.showerror("Error", "This is an error message.")

# Function to ask a yes/no question
def ask_yes_no_question():
    result = messagebox.askyesno("Question", "Do you want to proceed?")
    if result:
        print("User clicked Yes.")
    else:
        print("User clicked No.")

# Create buttons to trigger message boxes
info_button = tk.Button(window, text="Info", command=show_info_message)
info_button.pack()

warning_button = tk.Button(window, text="Warning", command=show_warning_message)
warning_button.pack()

error_button = tk.Button(window, text="Error", command=show_error_message)
error_button.pack()

question_button = tk.Button(window, text="Question", command=ask_yes_no_question)
question_button.pack()

# Run the main event loop
window.mainloop()
