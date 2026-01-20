# ---------------------------------------------------------------------------
# Date: 2026-01-11
# Script Name: main.py
# Author: omegazyph
# Updated: 2026-01-19
# Description: This is a standalone Fuel Performance Tracker for trucking. 
#              It calculates Miles Per Gallon (MPG) and Fuel Cost Per Mile (CPM).
#              It saves results into a CSV spreadsheet for business records.
#              Added: Manual Date entry field (Defaults to today's date).
# ---------------------------------------------------------------------------

import tkinter as tk
from tkinter import messagebox
import os
import csv
from datetime import datetime

class FuelTrackerApplication:
    def __init__(self, root_window):
        """
        The constructor initializes the main window and sets up the 
        file paths and user interface components.
        """
        self.root_window = root_window
        self.root_window.title("omegazyph's Professional Fuel Performance Tracker")
        self.root_window.geometry("600x900") # Increased height for more fields
        self.root_window.configure(bg="#f0f0f0")

        # --- FILE PATH SETUP ---
        self.current_script_directory = os.path.dirname(os.path.abspath(__file__))
        self.project_base_directory = os.path.dirname(self.current_script_directory)
        self.data_storage_directory = os.path.join(self.project_base_directory, "data")
        self.spreadsheet_file_path = os.path.join(self.data_storage_directory, "fuel_history.csv")

        # --- USER INTERFACE HEADER ---
        self.label_main_header = tk.Label(
            self.root_window, 
            text="TRUCK FUEL PERFORMANCE TRACKER", 
            font=("Segoe UI", 18, "bold"), 
            bg="#f0f0f0", 
            fg="#2c3e50"
        )
        self.label_main_header.pack(pady=30)

        # --- INPUT CONTAINER FRAME ---
        self.input_fields_frame = tk.Frame(self.root_window, bg="#f0f0f0")
        self.input_fields_frame.pack(pady=10)

        self.input_label_style = {"bg": "#f0f0f0", "font": ("Segoe UI", 11, "bold")}

        # 0. DATE ENTRY (New Addition: Manual override)
        self.label_date_entry = tk.Label(self.input_fields_frame, text="Date (YYYY-MM-DD):", **self.input_label_style)
        self.label_date_entry.grid(row=0, column=0, sticky="e", pady=10, padx=10)
        
        self.entry_date_value = tk.Entry(self.input_fields_frame, font=("Segoe UI", 12), width=20)
        self.entry_date_value.grid(row=0, column=1, pady=10, padx=10)
        # Pre-fill with today's date as a helpful default
        self.entry_date_value.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # 1. LOAD NUMBER ENTRY
        self.label_load_number = tk.Label(self.input_fields_frame, text="Load Number / ID:", **self.input_label_style)
        self.label_load_number.grid(row=1, column=0, sticky="e", pady=10, padx=10)
        
        self.entry_load_number = tk.Entry(self.input_fields_frame, font=("Segoe UI", 12), width=20)
        self.entry_load_number.grid(row=1, column=1, pady=10, padx=10)

        # 2. STARTING ODOMETER ENTRY
        self.label_starting_odometer = tk.Label(self.input_fields_frame, text="Starting Odometer Reading:", **self.input_label_style)
        self.label_starting_odometer.grid(row=2, column=0, sticky="e", pady=10, padx=10)
        
        self.entry_starting_odometer = tk.Entry(self.input_fields_frame, font=("Segoe UI", 12), width=20)
        self.entry_starting_odometer.grid(row=2, column=1, pady=10, padx=10)

        # 3. ENDING ODOMETER ENTRY
        self.label_ending_odometer = tk.Label(self.input_fields_frame, text="Ending Odometer Reading:", **self.input_label_style)
        self.label_ending_odometer.grid(row=3, column=0, sticky="e", pady=10, padx=10)
        
        self.entry_ending_odometer = tk.Entry(self.input_fields_frame, font=("Segoe UI", 12), width=20)
        self.entry_ending_odometer.grid(row=3, column=1, pady=10, padx=10)

        # 4. FUEL GALLONS ENTRY
        self.label_fuel_gallons = tk.Label(self.input_fields_frame, text="Total Gallons Purchased:", **self.input_label_style)
        self.label_fuel_gallons.grid(row=4, column=0, sticky="e", pady=10, padx=10)
        
        self.entry_fuel_gallons = tk.Entry(self.input_fields_frame, font=("Segoe UI", 12), width=20)
        self.entry_fuel_gallons.grid(row=4, column=1, pady=10, padx=10)

        # 5. FUEL COST ENTRY
        self.label_total_fuel_cost = tk.Label(self.input_fields_frame, text="Total Fuel Cost (Dollars):", **self.input_label_style)
        self.label_total_fuel_cost.grid(row=5, column=0, sticky="e", pady=10, padx=10)
        
        self.entry_total_fuel_cost = tk.Entry(self.input_fields_frame, font=("Segoe UI", 12), width=20)
        self.entry_total_fuel_cost.grid(row=5, column=1, pady=10, padx=10)

        # --- ACTION BUTTONS CONTAINER ---
        self.button_container_frame = tk.Frame(self.root_window, bg="#f0f0f0")
        self.button_container_frame.pack(pady=20)

        self.button_perform_calculation = tk.Button(
            self.button_container_frame, 
            text="CALCULATE PERFORMANCE", 
            command=self.calculate_truck_performance, 
            bg="#0078d4", 
            fg="white", 
            font=("Segoe UI", 11, "bold"), 
            width=22
        )
        self.button_perform_calculation.grid(row=0, column=0, padx=10)

        self.button_reset_fields = tk.Button(
            self.button_container_frame, 
            text="RESET ALL FIELDS", 
            command=self.reset_all_input_fields, 
            bg="#d13438", 
            fg="white", 
            font=("Segoe UI", 11, "bold"), 
            width=22
        )
        self.button_reset_fields.grid(row=0, column=1, padx=10)

        # --- RESULTS DISPLAY SECTION ---
        self.label_total_miles_output = tk.Label(
            self.root_window, 
            text="Total Miles: Pending...", 
            font=("Segoe UI", 14, "bold"), 
            bg="#f0f0f0", 
            fg="#004e8c"
        )
        self.label_total_miles_output.pack(pady=5)

        self.label_mpg_output = tk.Label(
            self.root_window, 
            text="Miles Per Gallon: Pending...", 
            font=("Segoe UI", 14, "bold"), 
            bg="#f0f0f0", 
            fg="#004e8c"
        )
        self.label_mpg_output.pack(pady=5)

        self.label_cpm_output = tk.Label(
            self.root_window, 
            text="Fuel Cost Per Mile: Pending...", 
            font=("Segoe UI", 14, "bold"), 
            bg="#f0f0f0", 
            fg="#004e8c"
        )
        self.label_cpm_output.pack(pady=5)

        # --- SPREADSHEET SAVE BUTTON ---
        self.button_save_to_spreadsheet = tk.Button(
            self.root_window, 
            text="ADD TO SPREADSHEET (CSV)", 
            command=self.append_data_to_csv_file, 
            bg="#107c10", 
            fg="white", 
            font=("Segoe UI", 12, "bold"), 
            width=40,
            state="disabled"
        )
        self.button_save_to_spreadsheet.pack(pady=30)

        # Variables for calculated values
        self.final_total_trip_miles = 0.0
        self.final_calculated_mpg = 0.0
        self.final_calculated_cpm = 0.0

    def calculate_truck_performance(self):
        """
        Retrieves user input, performs the mathematical operations,
        and updates the display labels.
        """
        try:
            start_miles = float(self.entry_starting_odometer.get())
            end_miles = float(self.entry_ending_odometer.get())
            gallons = float(self.entry_fuel_gallons.get())
            dollars = float(self.entry_total_fuel_cost.get())

            self.final_total_trip_miles = end_miles - start_miles

            if self.final_total_trip_miles <= 0:
                messagebox.showerror("Mileage Error", "The ending odometer must be greater than the starting odometer.")
                return

            if gallons > 0:
                self.final_calculated_mpg = self.final_total_trip_miles / gallons
            else:
                self.final_calculated_mpg = 0.0

            if self.final_total_trip_miles > 0:
                self.final_calculated_cpm = dollars / self.final_total_trip_miles
            else:
                self.final_calculated_cpm = 0.0

            # Update results on screen
            self.label_total_miles_output.config(text=f"Total Miles: {self.final_total_trip_miles:.1f}")
            self.label_mpg_output.config(text=f"Miles Per Gallon: {self.final_calculated_mpg:.2f}")
            self.label_cpm_output.config(text=f"Fuel Cost Per Mile: ${self.final_calculated_cpm:.3f}")
            
            self.button_save_to_spreadsheet.config(state="normal")

        except ValueError:
            messagebox.showerror("Input Error", "Please ensure all mileage and cost fields contain numbers.")

    def reset_all_input_fields(self):
        """
        Clears every entry box and resets the calculation labels.
        """
        self.entry_date_value.delete(0, tk.END)
        # Re-insert today's date so the user doesn't have to type it every time
        self.entry_date_value.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        self.entry_load_number.delete(0, tk.END)
        self.entry_starting_odometer.delete(0, tk.END)
        self.entry_ending_odometer.delete(0, tk.END)
        self.entry_fuel_gallons.delete(0, tk.END)
        self.entry_total_fuel_cost.delete(0, tk.END)
        
        self.label_total_miles_output.config(text="Total Miles: Pending...")
        self.label_mpg_output.config(text="Miles Per Gallon: Pending...")
        self.label_cpm_output.config(text="Fuel Cost Per Mile: Pending...")
        
        self.button_save_to_spreadsheet.config(state="disabled")

    def append_data_to_csv_file(self):
        """
        Saves the current trip data into a CSV file inside the 'data' folder.
        """
        if not os.path.exists(self.data_storage_directory):
            os.makedirs(self.data_storage_directory)

        file_is_new = not os.path.isfile(self.spreadsheet_file_path)
        
        # Get the date from the entry box instead of the system clock
        user_specified_date = self.entry_date_value.get()

        # Create the data list for the CSV row
        data_row = [
            user_specified_date,
            self.entry_load_number.get(),
            self.entry_starting_odometer.get(),
            self.entry_ending_odometer.get(),
            format(self.final_total_trip_miles, ".1f"),
            self.entry_fuel_gallons.get(),
            self.entry_total_fuel_cost.get(),
            format(self.final_calculated_mpg, ".2f"),
            format(self.final_calculated_cpm, ".3f")
        ]

        try:
            with open(self.spreadsheet_file_path, mode='a', newline='') as csv_file_handler:
                csv_writer_object = csv.writer(csv_file_handler)
                
                if file_is_new:
                    csv_writer_object.writerow([
                        "Date", 
                        "Load ID", 
                        "Starting Miles", 
                        "Ending Miles", 
                        "Total Trip Miles", 
                        "Gallons Used", 
                        "Fuel Cost USD", 
                        "MPG", 
                        "Fuel CPM"
                    ])
                
                csv_writer_object.writerow(data_row)

            messagebox.showinfo("Save Successful", f"Trip data for Load {self.entry_load_number.get()} saved for {user_specified_date}.")
            self.button_save_to_spreadsheet.config(state="disabled")
            
        except Exception as error_exception:
            messagebox.showerror("File Error", f"An error occurred while saving: {error_exception}")

if __name__ == "__main__":
    main_tkinter_window = tk.Tk()
    tracker_application = FuelTrackerApplication(main_tkinter_window)
    main_tkinter_window.mainloop()