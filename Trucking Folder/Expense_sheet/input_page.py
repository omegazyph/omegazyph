import tkinter as tk
from tkinter import messagebox

class InputPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Input Page")
        self.geometry("400x300")
        self.label = tk.Label(self, text="Enter your Info", font=("Helvetica", 20))
        self.label.pack(pady=30)
        self.order = tk.Entry(self)
        self.order.insert(0, "Order#")
        self.order.pack()
        self.back_button = tk.Button(self, text="Back to Starting Page", command=self.open_starting_page)
        self.back_button.pack(side="left")
        self.submit_button = tk.Button(self, text="Submit", command=self.print_entry_text)
        self.submit_button.pack(side="right")

    def print_entry_text(self):
        order_text = self.order.get()
        if order_text == 'Order#' or order_text == "":
            self.show_alert()
        else:
            print(order_text)

    def show_alert(self):
        messagebox.showinfo("Alert", "Order number can not be empty")

    def open_starting_page(self):
        self.destroy()
        from starting_page import StartingPage
        StartingPage().mainloop()
