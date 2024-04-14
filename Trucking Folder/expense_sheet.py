import tkinter as tk

class StartingPage(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Welcome to Trucker Expense App")
        self.geometry("500x300")

        self.label = tk.Label(self, text="Welcome to Trucker Expense App", font=("Helvetica", 20))
        self.label.pack(pady=30)

        self.button = tk.Button(self, text="Press here to get started", command=self.open_next_page)
        self.button.pack()

    def open_next_page(self):
        self.destroy()  # Close the current window
        NextPage().mainloop()

class NextPage(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Next Page")
        self.geometry("400x300")

        self.label = tk.Label(self, text="This is the Next Page", font=("Helvetica", 20))
        self.label.pack(pady=30)

        self.button = tk.Button(self, text="Back to Starting Page", command=self.open_starting_page)
        self.button.pack()

    def open_starting_page(self):
        self.destroy()  # Close the current window
        StartingPage().mainloop()

if __name__ == "__main__":
    app = StartingPage()
    app.mainloop()
