import tkinter as tk  # Import the Tkinter module
from tkinter import messagebox

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

        #region Labals
        # Create a label widget
        self.label = tk.Label(self, text="Enter your Info", font=("Helvetica", 20))
        self.label.pack(pady=30)  # Pack the label widget into the window with some padding
        #endregion



        #region Entry Fields
        order = tk.Entry(self) #Order number 
        order.insert(0, "Order#")  # Set the initial value of the entry field
        order.pack()
        #endregion



        # region print text and alert
        def print_entry_text():
            order_text = order.get()  # Get the text from the entry field
            if order_text == 'Order#' or order_text == "":
                show_alert()
            else:
                print(order_text)  # Print the text to the console
        
        def show_alert():
            messagebox.showinfo("Alert", "Order number can not be empty")
        #endregion



        # region Buttons
        # Create a button widget
        self.back_button = tk.Button(self, text="Back to Starting Page", command=self.open_starting_page)
        self.back_button.pack(side="left")  # Pack the button widget into the window
        
        self.submit_button = tk.Button(self, text="Submit", command=print_entry_text) 
        self.submit_button.pack(side="right")  # Pack the button widget into the window
        # endregion



    def open_starting_page(self):  # Define a method to open the starting page
        self.destroy()  # Close the current window
        StartingPage().mainloop()  # Create an instance of the StartingPage class and run its event loop



if __name__ == "__main__":  # Check if the script is being run directly
    app = StartingPage()  # Create an instance of the StartingPage class
    app.mainloop()  # Run the event loop to display the window and handle user events
