# ---------------------------------------------------------------------------
# Date: 2026-01-11
# Script Name: main.py
# Author: omegazyph
# Updated: 2026-01-22
# Description: Main Graphical User Interface (GUI) for the Fuel Tracker.
#              Provides fields for Date, Load ID, Mileage, and Costs.
#              Includes 'Delete Last' button for error correction.
# ---------------------------------------------------------------------------

import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime
from fuel_logic import FuelDataManager  # Connecting to our logic script

class FuelTrackerApp:
    def __init__(self, root_window):
        """
        Setup the main window and initialize the data connection.
        """
        self.root = root_window
        self.root.title("omegazyph's Professional Fuel Tracker")
        self.root.geometry("600x950")  # Tall enough for all buttons
        self.root.configure(bg="#f0f0f0")

        # Dynamically find the path to the CSV file based on script location
        script_directory = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_directory)
        csv_full_path = os.path.join(project_root, "data", "fuel_history.csv")

        # Create an instance of our Logic Manager
        self.data_manager = FuelDataManager(csv_full_path)

        # Variables to hold math results globally within the class
        self.calculation_results = {"miles": 0.0, "mpg": 0.0, "cpm": 0.0}

        # Build the visual components
        self.initialize_user_interface()

    def initialize_user_interface(self):
        """
        Creates labels, entry boxes, and buttons.
        """
        tk.Label(self.root, text="TRUCK FUEL PERFORMANCE", 
                 font=("Segoe UI", 20, "bold"), bg="#f0f0f0", fg="#2c3e50").pack(pady=20)
        
        # Frame to organize inputs in a grid
        self.input_container = tk.Frame(self.root, bg="#f0f0f0")
        self.input_container.pack()

        # Creating the input fields using a helper method to keep code clean
        self.entry_date = self.add_labeled_entry("Date (YYYY-MM-DD):", 0)
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d")) # Default to today
        
        self.entry_load = self.add_labeled_entry("Load Number / ID:", 1)
        self.entry_start = self.add_labeled_entry("Starting Odometer:", 2)
        self.entry_end = self.add_labeled_entry("Ending Odometer:", 3)
        self.entry_gallons = self.add_labeled_entry("Total Gallons:", 4)
        self.entry_cost = self.add_labeled_entry("Total Cost ($):", 5)

        # Row of Action Buttons (Calculate and Reset)
        button_row = tk.Frame(self.root, bg="#f0f0f0")
        button_row.pack(pady=20)
        
        tk.Button(button_row, text="CALCULATE", command=self.perform_math, 
                  bg="#0078d4", fg="white", font=("Segoe UI", 10, "bold"), width=15).grid(row=0, column=0, padx=5)
        
        tk.Button(button_row, text="RESET FIELDS", command=self.clear_entries, 
                  bg="#a0a0a0", fg="white", font=("Segoe UI", 10, "bold"), width=15).grid(row=0, column=1, padx=5)

        # Area to display the calculated math results
        self.label_miles = tk.Label(self.root, text="Total Miles: --", font=("Segoe UI", 13), bg="#f0f0f0")
        self.label_miles.pack()
        self.label_mpg = tk.Label(self.root, text="MPG: --", font=("Segoe UI", 13), bg="#f0f0f0")
        self.label_mpg.pack()
        self.label_cpm = tk.Label(self.root, text="CPM: --", font=("Segoe UI", 13), bg="#f0f0f0")
        self.label_cpm.pack()

        # Save Button - Starts disabled until user calculates
        self.button_save = tk.Button(self.root, text="ADD TO SPREADSHEET (CSV)", 
                                     command=self.save_data, bg="#107c10", fg="white", 
                                     font=("Segoe UI", 12, "bold"), width=35, state="disabled")
        self.button_save.pack(pady=20)

        # THE FIX: Delete Last Entry Button
        tk.Button(self.root, text="DELETE LAST SAVED ENTRY", command=self.undo_last_save, 
                  bg="#d13438", fg="white", font=("Segoe UI", 9), width=25).pack(pady=10)

    def add_labeled_entry(self, label_text, row_index):
        """
        Utility function to create a label and an entry box in the grid.
        """
        tk.Label(self.input_container, text=label_text, bg="#f0f0f0", 
                 font=("Segoe UI", 11, "bold")).grid(row=row_index, column=0, sticky="e", pady=8, padx=10)
        new_entry = tk.Entry(self.input_container, font=("Segoe UI", 12), width=22)
        new_entry.grid(row=row_index, column=1, pady=8, padx=10)
        return new_entry

    def perform_math(self):
        """
        Pull values from screen and run the MPG/CPM formulas.
        """
        try:
            start_val = float(self.entry_start.get())
            end_val = float(self.entry_end.get())
            gal_val = float(self.entry_gallons.get())
            cost_val = float(self.entry_cost.get())

            # Distance Logic
            self.calculation_results["miles"] = end_val - start_val
            if self.calculation_results["miles"] <= 0:
                messagebox.showwarning("Logic Error", "Ending odometer must be higher than starting.")
                return

            # Economy Logic
            self.calculation_results["mpg"] = self.calculation_results["miles"] / gal_val if gal_val > 0 else 0
            self.calculation_results["cpm"] = cost_val / self.calculation_results["miles"] if self.calculation_results["miles"] > 0 else 0

            # Update Labels
            self.label_miles.config(text=f"Total Miles: {self.calculation_results['miles']:.1f}")
            self.label_mpg.config(text=f"MPG: {self.calculation_results['mpg']:.2f}")
            self.label_cpm.config(text=f"CPM: ${self.calculation_results['cpm']:.3f}")
            
            # Allow user to save now that math is done
            self.button_save.config(state="normal")
        except ValueError:
            messagebox.showerror("Input Error", "Please fill all mileage and cost fields with numbers.")

    def save_data(self):
        """
        Format the data and send it to the Logic Manager for sorting and saving.
        """
        data_list = [
            self.entry_date.get(),
            self.entry_load.get(),
            self.entry_start.get(),
            self.entry_end.get(),
            f"{self.calculation_results['miles']:.1f}",
            self.entry_gallons.get(),
            self.entry_cost.get(),
            f"{self.calculation_results['mpg']:.2f}",
            f"{self.calculation_results['cpm']:.3f}"
        ]
        self.data_manager.save_and_sort_data(data_list)
        messagebox.showinfo("Success", f"Load {self.entry_load.get()} saved and sorted.")
        self.button_save.config(state="disabled")

    def undo_last_save(self):
        """
        Calls the delete logic if the user made a mistake.
        """
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to remove the last entry from the CSV?")
        if confirm:
            success, message = self.data_manager.delete_last_saved_entry()
            if success:
                messagebox.showinfo("Deleted", message)
            else:
                messagebox.showwarning("Attention", message)

    def clear_entries(self):
        """
        Wipes the screen clean for a new load.
        """
        for entry in [self.entry_load, self.entry_start, self.entry_end, self.entry_gallons, self.entry_cost]:
            entry.delete(0, tk.END)
        self.button_save.config(state="disabled")

if __name__ == "__main__":
    main_window = tk.Tk()
    tracker_app = FuelTrackerApp(main_window)
    main_window.mainloop()