# main.py

import tkinter as tk
from tkinter import ttk
from investment_calculator import (
    calculate_compound_interest,
    calculate_future_value,
    calculate_annualized_return
)

class InvestmentGuideApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Beginner Investment Guide")

        # Create and configure the main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Labels and Entries for User Inputs
        ttk.Label(self.main_frame, text="Principal Amount:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.principal_entry = ttk.Entry(self.main_frame)
        self.principal_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.main_frame, text="Annual Interest Rate (%):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.rate_entry = ttk.Entry(self.main_frame)
        self.rate_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.main_frame, text="Times Compounded Per Year:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.compound_entry = ttk.Entry(self.main_frame)
        self.compound_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.main_frame, text="Number of Years:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.years_entry = ttk.Entry(self.main_frame)
        self.years_entry.grid(row=3, column=1, padx=5, pady=5)

        # Buttons
        ttk.Button(self.main_frame, text="Calculate Compound Interest", command=self.calculate_compound_interest).grid(row=4, column=0, columnspan=2, padx=5, pady=10)

        # Result Display
        self.result_label = ttk.Label(self.main_frame, text="", wraplength=300)
        self.result_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def calculate_compound_interest(self):
        try:
            principal = float(self.principal_entry.get())
            rate = float(self.rate_entry.get()) / 100
            times_compounded = int(self.compound_entry.get())
            years = int(self.years_entry.get())

            compound_interest = calculate_compound_interest(principal, rate, times_compounded, years)
            future_value = calculate_future_value(principal, rate, times_compounded, years)
            annualized_return = calculate_annualized_return(principal, future_value, years)

            result_text = (f"Compound Interest: ${compound_interest:.2f}\n"
                           f"Future Value: ${future_value:.2f}\n"
                           f"Annualized Return: {annualized_return:.2%}")

            self.result_label.config(text=result_text)
        except ValueError:
            self.result_label.config(text="Please enter valid numerical values.")

if __name__ == "__main__":
    root = tk.Tk()
    app = InvestmentGuideApp(root)
    root.mainloop()
