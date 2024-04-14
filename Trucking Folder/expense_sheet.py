import tkinter as tk  # Import the Tkinter module

class StartingPage(tk.Tk):  # Define a class for the starting page, inheriting from Tkinter's Tk class
    def __init__(self):
        super().__init__()  # Initialize the parent class (Tk)

        self.title("Welcome to Trucker Expense App")  # Set the title of the window
        self.geometry("500x300")  # Set the size of the window

        self.label = tk.Label(self, text="Welcome to Trucker Expense App", font=("Helvetica", 20))  # Create a label widget
        self.label.pack(pady=30)  # Pack the label widget into the window with some padding

        self.button = tk.Button(self, text="Press here to get started", command=self.open_next_page)  # Create a button widget
        self.button.pack()  # Pack the button widget into the window

    def open_next_page(self):  # Define a method to open the next page
        self.destroy()  # Close the current window
        NextPage().mainloop()  # Create an instance of the NextPage class and run its event loop

class NextPage(tk.Tk):  # Define a class for the next page, inheriting from Tkinter's Tk class
    def __init__(self):
        super().__init__()  # Initialize the parent class (Tk)

        self.title("Next Page")  # Set the title of the window
        self.geometry("400x300")  # Set the size of the window

        self.label = tk.Label(self, text="This is the Next Page", font=("Helvetica", 20))  # Create a label widget
        self.label.pack(pady=30)  # Pack the label widget into the window with some padding

        self.button = tk.Button(self, text="Back to Starting Page", command=self.open_starting_page)  # Create a button widget
        self.button.pack()  # Pack the button widget into the window

    def open_starting_page(self):  # Define a method to open the starting page
        self.destroy()  # Close the current window
        StartingPage().mainloop()  # Create an instance of the StartingPage class and run its event loop

if __name__ == "__main__":  # Check if the script is being run directly
    app = StartingPage()  # Create an instance of the StartingPage class
    app.mainloop()  # Run the event loop to display the window and handle user events
