# ---------------------------------------------------------------------------
# Date: 2026-01-11
# Script Name: main.py
# Author: omegazyph
# Updated: 2026-01-19
# Description: This is a standalone Fuel Performance Tracker for trucking. 
#              It calculates Miles Per Gallon (MPG) and Fuel Cost Per Mile (CPM).
#              It saves results into a CSV spreadsheet for business records.
#              All code is written in full, non-shorthand format.
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
        # Set the main window as a property of the class
        self.root_window = root_window
        
        # Set the window title for the Lenovo Legion display
        self.root_window.title("omegazyph's Professional Fuel Performance Tracker")
        
        # Define the window dimensions
        self.root_window.geometry("600x750")
        
        # Set the background color to a light grey
        self.root_window.configure(bg="#f0f0f0")

        # --- FILE PATH SETUP ---
        # Get the absolute path of the directory where this script is located
        self.current_script_directory = os.path.dirname(os.path.abspath(__file__))
        
        # Move up one level to the main project folder
        self.project_base_directory = os.path.dirname(self.current_script_directory)
        
        # Define the path for the 'data' folder
        self.data_storage_directory = os.path.join(self.project_base_directory, "data")
        
        # Define the path for the CSV spreadsheet file
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

        # Standard font style for all input labels
        self.input_label_style = {"bg": "#f0f0f0", "font": ("Segoe UI", 11, "bold")}

        # 1. STARTING ODOMETER ENTRY
        self.label_starting_odometer = tk.Label(self.input_fields_frame, text="Starting Odometer Reading:", **self.input_label_style)
        self.label_starting_odometer.grid(row=0, column=0, sticky="e", pady=10, padx=10)
        
        self.entry_starting_odometer = tk.Entry(self.input_fields_frame, font=("Segoe UI", 12), width=20)
        self.entry_starting_odometer.grid(row=0, column=1, pady=10, padx=10)

        # 2. ENDING ODOMETER ENTRY
        self.label_ending_odometer = tk.Label(self.input_fields_frame, text="Ending Odometer Reading:", **self.input_label_style)
        self.label_ending_odometer.grid(row=1, column=0, sticky="e", pady=10, padx=10)
        
        self.entry_ending_odometer = tk.Entry(self.input_fields_frame, font=("Segoe UI", 12), width=20)
        self.entry_ending_odometer.grid(row=1, column=1, pady=10, padx=10)

        # 3. FUEL GALLONS ENTRY
        self.label_fuel_gallons = tk.Label(self.input_fields_frame, text="Total Gallons Purchased:", **self.input_label_style)
        self.label_fuel_gallons.grid(row=2, column=0, sticky="e", pady=10, padx=10)
        
        self.entry_fuel_gallons = tk.Entry(self.input_fields_frame, font=("Segoe UI", 12), width=20)
        self.entry_fuel_gallons.grid(row=2, column=1, pady=10, padx=10)

        # 4. FUEL COST ENTRY
        self.label_total_fuel_cost = tk.Label(self.input_fields_frame, text="Total Fuel Cost (Dollars):", **self.input_label_style)
        self.label_total_fuel_cost.grid(row=3, column=0, sticky="e", pady=10, padx=10)
        
        self.entry_total_fuel_cost = tk.Entry(self.input_fields_frame, font=("Segoe UI", 12), width=20)
        self.entry_total_fuel_cost.grid(row=3, column=1, pady=10, padx=10)

        # --- ACTION BUTTONS CONTAINER ---
        self.button_container_frame = tk.Frame(self.root_window, bg="#f0f0f0")
        self.button_container_frame.pack(pady=20)

        # CALCULATE BUTTON
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

        # RESET BUTTON
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
        self.label_mpg_output = tk.Label(
            self.root_window, 
            text="Miles Per Gallon: Pending...", 
            font=("Segoe UI", 14, "bold"), 
            bg="#f0f0f0", 
            fg="#004e8c"
        )
        self.label_mpg_output.pack(pady=10)

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

        # Variables to store mathematical results for the spreadsheet
        self.final_calculated_mpg = 0.0
        self.final_calculated_cpm = 0.0

    def calculate_truck_performance(self):
        """
        Retrieves user input, performs the mathematical division for 
        MPG and CPM, and updates the display labels.
        """
        try:
            # Step 1: Extract numeric data from the entry boxes
            start_miles = float(self.entry_starting_odometer.get())
            end_miles = float(self.entry_ending_odometer.get())
            gallons = float(self.entry_fuel_gallons.get())
            dollars = float(self.entry_total_fuel_cost.get())

            # Step 2: Determine total distance
            total_trip_distance = end_miles - start_miles

            # Step 3: Validate distance
            if total_trip_distance <= 0:
                messagebox.showerror("Mileage Error", "The ending odometer must be greater than the starting odometer.")
                return

            # Step 4: Perform mathematical operations
            if gallons > 0:
                self.final_calculated_mpg = total_trip_distance / gallons
            else:
                self.final_calculated_mpg = 0.0

            if total_trip_distance > 0:
                self.final_calculated_cpm = dollars / total_trip_distance
            else:
                self.final_calculated_cpm = 0.0

            # Step 5: Update the labels on the interface
            self.label_mpg_output.config(text=f"Miles Per Gallon: {self.final_calculated_mpg:.2f}")
            self.label_cpm_output.config(text=f"Fuel Cost Per Mile: ${self.final_calculated_cpm:.3f}")
            
            # Step 6: Enable the save button
            self.button_save_to_spreadsheet.config(state="normal")

        except ValueError:
            messagebox.showerror("Input Error", "Please ensure all fields contain only numeric values.")

    def reset_all_input_fields(self):
        """
        Clears every entry box and resets the calculation labels.
        """
        self.entry_starting_odometer.delete(0, tk.END)
        self.entry_ending_odometer.delete(0, tk.END)
        self.entry_fuel_gallons.delete(0, tk.END)
        self.entry_total_fuel_cost.delete(0, tk.END)
        
        self.label_mpg_output.config(text="Miles Per Gallon: Pending...")
        self.label_cpm_output.config(text="Fuel Cost Per Mile: Pending...")
        
        self.button_save_to_spreadsheet.config(state="disabled")

    def append_data_to_csv_file(self):
        """
        Saves the current trip data into a CSV file inside the 'data' folder.
        """
        # Ensure the data directory exists
        if not os.path.exists(self.data_storage_directory):
            os.makedirs(self.data_storage_directory)

        # Determine if we need to write the header row
        file_is_new = not os.path.isfile(self.spreadsheet_file_path)

        # Gather the current date and time
        current_date_and_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create the data list for the CSV row
        data_row = [
            current_date_and_time,
            self.entry_starting_odometer.get(),
            self.entry_ending_odometer.get(),
            self.entry_fuel_gallons.get(),
            self.entry_total_fuel_cost.get(),
            format(self.final_calculated_mpg, ".2f"),
            format(self.final_calculated_cpm, ".3f")
        ]

        try:
            # Open the file in append mode
            with open(self.spreadsheet_file_path, mode='a', newline='') as csv_file_handler:
                csv_writer_object = csv.writer(csv_file_handler)
                
                # Write header if this is a brand new file
                if file_is_new:
                    csv_writer_object.writerow([
                        "Date and Time", 
                        "Starting Miles", 
                        "Ending Miles", 
                        "Gallons Used", 
                        "Fuel Cost USD", 
                        "MPG", 
                        "Fuel CPM"
                    ])
                
                # Write the actual data
                csv_writer_object.writerow(data_row)

            messagebox.showinfo("Save Successful", f"Data has been added to:\n{self.spreadsheet_file_path}")
            
            # Disable the button after saving to avoid duplicate entries
            self.button_save_to_spreadsheet.config(state="disabled")
            
        except Exception as error_exception:
            messagebox.showerror("File Error", f"An error occurred while saving: {error_exception}")

# --- START THE APPLICATION ---
if __name__ == "__main__":
    # Create the root window instance
    main_tkinter_window = tk.Tk()
    
    # Initialize the Fuel Tracker Application
    tracker_application = FuelTrackerApplication(main_tkinter_window)
    
    # Run the graphical user interface loop
    main_tkinter_window.mainloop()