# ---------------------------------------------------------------------------
# Date: 2026-01-11
# Script Name: main.py
# Author: omegazyph
# Updated: 2026-01-21
# Description: Main GUI for the Fuel Tracker. Imports logic from fuel_logic.py.
# ---------------------------------------------------------------------------

import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime
from fuel_logic import FuelDataManager # Importing our logic class

class FuelTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("omegazyph's Professional Fuel Tracker")
        self.root.geometry("600x900")
        self.root.configure(bg="#f0f0f0")

        # Set up file paths
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(script_dir)
        csv_path = os.path.join(project_dir, "data", "fuel_history.csv")

        # Initialize the logic manager
        self.data_manager = FuelDataManager(csv_path)

        # Create UI
        self.setup_ui()

    def setup_ui(self):
        """Builds all the entry fields and labels."""
        tk.Label(self.root, text="TRUCK FUEL PERFORMANCE", font=("Segoe UI", 18, "bold"), bg="#f0f0f0").pack(pady=20)
        
        self.fields_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.fields_frame.pack()

        label_style = {"bg": "#f0f0f0", "font": ("Segoe UI", 11, "bold")}
        
        # Input fields
        self.entry_date = self.create_input("Date (YYYY-MM-DD):", 0)
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        self.entry_load = self.create_input("Load Number / ID:", 1)
        self.entry_start = self.create_input("Starting Odometer:", 2)
        self.entry_end = self.create_input("Ending Odometer:", 3)
        self.entry_gallons = self.create_input("Total Gallons:", 4)
        self.entry_cost = self.create_input("Total Cost ($):", 5)

        # Calculate and Reset Buttons
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="CALCULATE", command=self.calculate, bg="#0078d4", fg="white", width=15).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="RESET", command=self.reset, bg="#d13438", fg="white", width=15).grid(row=0, column=1, padx=5)

        # Output Labels
        self.lbl_miles = tk.Label(self.root, text="Total Miles: --", font=("Segoe UI", 12), bg="#f0f0f0")
        self.lbl_miles.pack()
        self.lbl_mpg = tk.Label(self.root, text="MPG: --", font=("Segoe UI", 12), bg="#f0f0f0")
        self.lbl_mpg.pack()
        self.lbl_cpm = tk.Label(self.root, text="CPM: --", font=("Segoe UI", 12), bg="#f0f0f0")
        self.lbl_cpm.pack()

        # Save Button
        self.btn_save = tk.Button(self.root, text="ADD TO SPREADSHEET (CSV)", command=self.save, bg="#107c10", fg="white", font=("Segoe UI", 12, "bold"), width=35, state="disabled")
        self.btn_save.pack(pady=20)

        # Values for saving
        self.results = {"miles": 0.0, "mpg": 0.0, "cpm": 0.0}

    def create_input(self, text, row):
        tk.Label(self.fields_frame, text=text, bg="#f0f0f0", font=("Segoe UI", 11, "bold")).grid(row=row, column=0, sticky="e", pady=5, padx=5)
        entry = tk.Entry(self.fields_frame, font=("Segoe UI", 12), width=20)
        entry.grid(row=row, column=1, pady=5, padx=5)
        return entry

    def calculate(self):
        try:
            start = float(self.entry_start.get())
            end = float(self.entry_end.get())
            gals = float(self.entry_gallons.get())
            cost = float(self.entry_cost.get())

            self.results["miles"] = end - start
            if self.results["miles"] <= 0:
                messagebox.showerror("Error", "Check odometer readings.")
                return

            self.results["mpg"] = self.results["miles"] / gals if gals > 0 else 0
            self.results["cpm"] = cost / self.results["miles"] if self.results["miles"] > 0 else 0

            self.lbl_miles.config(text=f"Total Miles: {self.results['miles']:.1f}")
            self.lbl_mpg.config(text=f"MPG: {self.results['mpg']:.2f}")
            self.lbl_cpm.config(text=f"CPM: ${self.results['cpm']:.3f}")
            self.btn_save.config(state="normal")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")

    def save(self):
        row = [
            self.entry_date.get(),
            self.entry_load.get(),
            self.entry_start.get(),
            self.entry_end.get(),
            f"{self.results['miles']:.1f}",
            self.entry_gallons.get(),
            self.entry_cost.get(),
            f"{self.results['mpg']:.2f}",
            f"{self.results['cpm']:.3f}"
        ]
        self.data_manager.save_and_sort_data(row)
        messagebox.showinfo("Success", "Record saved and sorted.")
        self.btn_save.config(state="disabled")

    def reset(self):
        for entry in [self.entry_load, self.entry_start, self.entry_end, self.entry_gallons, self.entry_cost]:
            entry.delete(0, tk.END)
        self.btn_save.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = FuelTrackerApp(root)
    root.mainloop()