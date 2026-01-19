# ---------------------------------------------------------------------------
# Date: 2026-01-11
# Script Name: main.py
# Author: omegazyph
# Updated: 2026-01-19
# Description: Standalone Fuel Performance Tracker. 
#              Calculates MPG and Fuel CPM from raw data.
#              Saves results into a CSV spreadsheet for long-term tracking.
# ---------------------------------------------------------------------------

import tkinter as tk
from tkinter import messagebox
import os
import csv
from datetime import datetime

class FuelTracker:
    def __init__(self, root):
        """
        The __init__ method sets up the main window and all the 
        visual elements (labels, entries, and buttons).
        """
        # Assign the main window to self.root
        self.root = root
        self.root.title("omegazyph's Fuel Performance Tracker")
        self.root.geometry("600x750") 
        self.root.configure(bg="#f0f0f0")

        # --- FOLDER AND CSV SETUP ---
        # Get the path where this script is located
        self.base_directory = os.path.dirname(os.path.dirname(__file__))
        # Define the path for the data folder
        self.data_directory = os.path.join(self.base_directory, "data")
        # Define the path for the CSV file
        self.csv_file_path = os.path.join(self.data_directory, "fuel_history.csv")

        # --- HEADER SECTION ---
        self.label_header = tk.Label(
            self.root, 
            text="TRUCK FUEL PERFORMANCE", 
            font=("Segoe UI", 18, "bold"), 
            bg="#f0f0f0", 
            fg="#333333"
        )
        self.label_header.pack(pady=20)

        # --- INPUT CONTAINER ---
        self.input_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.input_frame.pack(pady=10)

        # --- INPUT FIELDS ---
        self.label_starting_miles = tk.Label(self.input_frame, text="Starting Mileage:", font=("Segoe UI", 11, "bold"), bg="#f0f0f0")
        self.label_starting_miles.grid(row=0, column=0, sticky="e", pady=10, padx=10)
        self.entry_starting_miles = tk.Entry(self.input_frame, font=("Segoe UI", 12), width=20)
        self.entry_starting_miles.grid(row=0, column=1, pady=10, padx=10)

        self.label_ending_miles = tk.Label(self.input_frame, text="Ending Mileage:", font=("Segoe UI", 11, "bold"), bg="#f0f0f0")
        self.label_ending_miles.grid(row=1, column=0, sticky="e", pady=10, padx=10)
        self.entry_ending_miles = tk.Entry(self.input_frame, font=("Segoe UI", 12), width=20)
        self.entry_ending_miles.grid(row=1, column=1, pady=10, padx=10)

        self.label_fuel_gallons = tk.Label(self.input_frame, text="Amount of Fuel (Gallons):", font=("Segoe UI", 11, "bold"), bg="#f0f0f0")
        self.label_fuel_gallons.grid(row=2, column=0, sticky="e", pady=10, padx=10)
        self.entry_fuel_gallons = tk.Entry(self.input_frame, font=("Segoe UI", 12), width=20)
        self.entry_fuel_gallons.grid(row=2, column=1, pady=10, padx=10)

        self.label_fuel_cost = tk.Label(self.input_frame, text="Cost of Fuel ($):", font=("Segoe UI", 11, "bold"), bg="#f0f0f0")
        self.label_fuel_cost.grid(row=3, column=0, sticky="e", pady=10, padx=10)
        self.entry_fuel_cost = tk.Entry(self.input_frame, font=("Segoe UI", 12), width=20)
        self.entry_fuel_cost.grid(row=3, column=1, pady=10, padx=10)

        # --- BUTTON CONTAINER ---
        self.button_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.button_frame.pack(pady=20)

        self.button_calculate = tk.Button(self.button_frame, text="CALCULATE", command=self.perform_calculations, bg="#0078d4", fg="white", font=("Segoe UI", 12, "bold"), width=15)
        self.button_calculate.grid(row=0, column=0, padx=10)

        self.button_reset = tk.Button(self.button_frame, text="RESET", command=self.reset_all_fields, bg="#d13438", fg="white", font=("Segoe UI", 12, "bold"), width=15)
        self.button_reset.grid(row=0, column=1, padx=10)

        # --- RESULTS AREA ---
        self.label_mpg_result = tk.Label(self.root, text="Miles Per Gallon: --", font=("Segoe UI", 14, "bold"), bg="#f0f0f0", fg="#004e8c")
        self.label_mpg_result.pack(pady=10)

        self.label_cpm_result = tk.Label(self.root, text="Fuel Cost Per Mile: --", font=("Segoe UI", 14, "bold"), bg="#f0f0f0", fg="#004e8c")
        self.label_cpm_result.pack(pady=5)

        # --- CSV SAVE FEATURE ---
        self.button_save = tk.Button(
            self.root, 
            text="ADD TO SPREADSHEET (CSV)", 
            command=self.save_to_csv, 
            bg="#01dd01", 
            fg="white", 
            font=("Segoe UI", 12, "bold"), 
            width=32,
            state="disabled"
        )
        self.button_save.pack(pady=20)

        # Keep track of calculated values for saving
        self.calculated_mpg = 0.0
        self.calculated_cpm = 0.0

    def perform_calculations(self):
        """Handles the math and enables the save button if valid."""
        try:
            starting_odometer = float(self.entry_starting_miles.get())
            ending_odometer = float(self.entry_ending_miles.get())
            gallons_pumped = float(self.entry_fuel_gallons.get())
            total_cost_paid = float(self.entry_fuel_cost.get())

            total_miles_driven = ending_odometer - starting_odometer

            if total_miles_driven <= 0:
                messagebox.showerror("Mileage Error", "Ending mileage must be higher than starting mileage.")
                return

            self.calculated_mpg = total_miles_driven / gallons_pumped if gallons_pumped > 0 else 0.0
            self.calculated_cpm = total_cost_paid / total_miles_driven if total_miles_driven > 0 else 0.0

            self.label_mpg_result.config(text=f"Miles Per Gallon: {self.calculated_mpg:.2f}")
            self.label_cpm_result.config(text=f"Fuel Cost Per Mile: ${self.calculated_cpm:.3f}")
            
            self.button_save.config(state="normal")

        except ValueError:
            messagebox.showerror("Input Error", "Please ensure all fields contain only numbers.")

    def reset_all_fields(self):
        """Clears all text and resets the UI."""
        self.entry_starting_miles.delete(0, tk.END)
        self.entry_ending_miles.delete(0, tk.END)
        self.entry_fuel_gallons.delete(0, tk.END)
        self.entry_fuel_cost.delete(0, tk.END)
        self.label_mpg_result.config(text="Miles Per Gallon: --")
        self.label_cpm_result.config(text="Fuel Cost Per Mile: --")
        self.button_save.config(state="disabled")

    def save_to_csv(self):
        """
        Appends the current trip data to a CSV file. 
        Creates the file and header if it does not exist.
        """
        # Ensure the data directory exists
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)

        # Check if we need to write a header (if file is new)
        file_exists = os.path.isfile(self.csv_file_path)

        # Prepare the data row
        row_data = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            self.entry_starting_miles.get(),
            self.entry_ending_miles.get(),
            self.entry_fuel_gallons.get(),
            self.entry_fuel_cost.get(),
            f"{self.calculated_mpg:.2f}",
            f"{self.calculated_cpm:.3f}"
        ]

        try:
            # Open file in 'append' mode (a) so we don't overwrite previous logs
            with open(self.csv_file_path, mode='a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                
                # Write header only if the file is being created for the first time
                if not file_exists:
                    writer.writerow(["Timestamp", "Start Miles", "End Miles", "Gallons", "Cost", "MPG", "Fuel CPM"])
                
                # Write the trip data
                writer.writerow(row_data)

            messagebox.showinfo("Success", f"Trip added to spreadsheet:\n{self.csv_file_path}")
            # Disable save button after saving to prevent duplicate entries
            self.button_save.config(state="disabled")
            
        except Exception as error_message:
            messagebox.showerror("CSV Error", f"Could not save to spreadsheet: {error_message}")

if __name__ == "__main__":
    main_window = tk.Tk()
    application_instance = FuelTracker(main_window)
    main_window.mainloop()