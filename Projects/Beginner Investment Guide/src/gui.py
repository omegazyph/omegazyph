import tkinter as tk
from tkinter import ttk

class InvestmentGuideApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Beginner Investment Guide")

        # Create and configure the main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Add a label
        self.label = ttk.Label(self.main_frame, text="Welcome to the Beginner Investment Guide!")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        # Add a button
        self.button = ttk.Button(self.main_frame, text="Get Investment Advice", command=self.get_advice)
        self.button.grid(row=1, column=0, padx=10, pady=10)

    def get_advice(self):
        # This is where you would add functionality to get investment advice
        self.label.config(text="Functionality to get investment advice goes here.")

if __name__ == "__main__":
    root = tk.Tk()
    app = InvestmentGuideApp(root)
    root.mainloop()
