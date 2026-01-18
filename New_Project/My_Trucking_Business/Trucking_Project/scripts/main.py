# ---------------------------------------------------------------------------
# Date: 2026-01-11
# Script Name: main.py
# Author: omegazyph
# Updated: 2026-01-17
# Description: This is a standalone Fuel Performance Tracker. 
#              It calculates Miles Per Gallon (MPG) and Fuel Cost Per Mile (CPM)
#              using raw odometer readings and fuel receipt data.
#              This version includes explicit comments and a reset function.
# ---------------------------------------------------------------------------

import tkinter as tk
from tkinter import messagebox

class FuelTracker:
    def __init__(self, root):
        """
        The __init__ method sets up the main window and all the 
        visual elements (labels, entries, and buttons).
        """
        # Assign the main window to self.root
        self.root = root
        
        # Set the title that appears at the top of the window
        self.root.title("omegazyph's Fuel Performance Tracker")
        
        # Set the starting size of the window (Width x Height)
        self.root.geometry("600x650")
        
        # Set the background color for the main window
        self.root.configure(bg="#f0f0f0")

        # --- HEADER SECTION ---
        # This is the main title shown at the top of the application
        self.label_header = tk.Label(
            self.root, 
            text="TRUCK FUEL PERFORMANCE", 
            font=("Segoe UI", 18, "bold"), 
            bg="#f0f0f0", 
            fg="#333333"
        )
        self.label_header.pack(pady=20)

        # --- INPUT CONTAINER ---
        # We use a Frame to group the input fields together neatly
        self.input_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.input_frame.pack(pady=10)

        # --- STARTING MILEAGE INPUT ---
        self.label_starting_miles = tk.Label(
            self.input_frame, 
            text="Starting Mileage:", 
            font=("Segoe UI", 11, "bold"), 
            bg="#f0f0f0"
        )
        self.label_starting_miles.grid(row=0, column=0, sticky="e", pady=10, padx=10)
        
        self.entry_starting_miles = tk.Entry(self.input_frame, font=("Segoe UI", 12), width=20)
        self.entry_starting_miles.grid(row=0, column=1, pady=10, padx=10)

        # --- ENDING MILEAGE INPUT ---
        self.label_ending_miles = tk.Label(
            self.input_frame, 
            text="Ending Mileage:", 
            font=("Segoe UI", 11, "bold"), 
            bg="#f0f0f0"
        )
        self.label_ending_miles.grid(row=1, column=0, sticky="e", pady=10, padx=10)
        
        self.entry_ending_miles = tk.Entry(self.input_frame, font=("Segoe UI", 12), width=20)
        self.entry_ending_miles.grid(row=1, column=1, pady=10, padx=10)

        # --- FUEL GALLONS INPUT ---
        self.label_fuel_gallons = tk.Label(
            self.input_frame, 
            text="Amount of Fuel (Gallons):", 
            font=("Segoe UI", 11, "bold"), 
            bg="#f0f0f0"
        )
        self.label_fuel_gallons.grid(row=2, column=0, sticky="e", pady=10, padx=10)
        
        self.entry_fuel_gallons = tk.Entry(self.input_frame, font=("Segoe UI", 12), width=20)
        self.entry_fuel_gallons.grid(row=2, column=1, pady=10, padx=10)

        # --- FUEL COST INPUT ---
        self.label_fuel_cost = tk.Label(
            self.input_frame, 
            text="Cost of Fuel ($):", 
            font=("Segoe UI", 11, "bold"), 
            bg="#f0f0f0"
        )
        self.label_fuel_cost.grid(row=3, column=0, sticky="e", pady=10, padx=10)
        
        self.entry_fuel_cost = tk.Entry(self.input_frame, font=("Segoe UI", 12), width=20)
        self.entry_fuel_cost.grid(row=3, column=1, pady=10, padx=10)

        # --- BUTTON CONTAINER ---
        # This frame holds the Calculate and Reset buttons side-by-side
        self.button_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.button_frame.pack(pady=20)

        # Calculate Button: Triggers the perform_calculations method
        self.button_calculate = tk.Button(
            self.button_frame, 
            text="CALCULATE", 
            command=self.perform_calculations, 
            bg="#0078d4", 
            fg="white", 
            font=("Segoe UI", 12, "bold"), 
            width=15
        )
        self.button_calculate.grid(row=0, column=0, padx=10)

        # Reset Button: Triggers the reset_all_fields method
        self.button_reset = tk.Button(
            self.button_frame, 
            text="RESET", 
            command=self.reset_all_fields, 
            bg="#d13438", 
            fg="white", 
            font=("Segoe UI", 12, "bold"), 
            width=15
        )
        self.button_reset.grid(row=0, column=1, padx=10)

        # --- RESULTS AREA ---
        # Labels used to display the final calculated values to the user
        self.label_mpg_result = tk.Label(
            self.root, 
            text="Miles Per Gallon: --", 
            font=("Segoe UI", 14, "bold"), 
            bg="#f0f0f0",
            fg="#004e8c"
        )
        self.label_mpg_result.pack(pady=10)

        self.label_cpm_result = tk.Label(
            self.root, 
            text="Fuel Cost Per Mile: --", 
            font=("Segoe UI", 14, "bold"), 
            bg="#f0f0f0",
            fg="#004e8c"
        )
        self.label_cpm_result.pack(pady=5)

    def perform_calculations(self):
        """
        This method handles the math logic. It pulls data from the entries,
        checks for errors, and calculates the MPG and CPM.
        """
        try:
            # Step 1: Get data from entries and convert to float (decimal) numbers
            starting_odometer = float(self.entry_starting_miles.get())
            ending_odometer = float(self.entry_ending_miles.get())
            gallons_pumped = float(self.entry_fuel_gallons.get())
            total_cost_paid = float(self.entry_fuel_cost.get())

            # Step 2: Calculate total distance traveled
            total_miles_driven = ending_odometer - starting_odometer

            # Step 3: Check if mileage is valid (End must be higher than Start)
            if total_miles_driven <= 0:
                messagebox.showerror("Mileage Error", "Ending mileage must be higher than starting mileage.")
                return

            # Step 4: Calculate Miles Per Gallon (Total Miles / Gallons)
            if gallons_pumped > 0:
                miles_per_gallon = total_miles_driven / gallons_pumped
            else:
                miles_per_gallon = 0.0

            # Step 5: Calculate Cost Per Mile (Total Cost / Total Miles)
            if total_miles_driven > 0:
                cost_per_mile = total_cost_paid / total_miles_driven
            else:
                cost_per_mile = 0.0

            # Step 6: Update the labels on the screen with formatted strings
            # :.2f means 2 decimal places, :.3f means 3 decimal places
            self.label_mpg_result.config(text=f"Miles Per Gallon: {miles_per_gallon:.2f}")
            self.label_cpm_result.config(text=f"Fuel Cost Per Mile: ${cost_per_mile:.3f}")

        except ValueError:
            # This catches cases where the user leaves a box empty or types letters
            messagebox.showerror("Input Error", "Please ensure all fields contain only numbers.")

    def reset_all_fields(self):
        """
        This method clears all text from the screen to allow for a new entry.
        """
        # Clear Entry fields from position 0 to the END
        self.entry_starting_miles.delete(0, tk.END)
        self.entry_ending_miles.delete(0, tk.END)
        self.entry_fuel_gallons.delete(0, tk.END)
        self.entry_fuel_cost.delete(0, tk.END)

        # Reset the result labels back to their default text
        self.label_mpg_result.config(text="Miles Per Gallon: --")
        self.label_cpm_result.config(text="Fuel Cost Per Mile: --")

# --- MAIN EXECUTION ---
# This block runs the application when the script is executed directly
if __name__ == "__main__":
    # Create the root Tkinter window object
    main_window = tk.Tk()
    
    # Instantiate our class and pass in the main window
    application_instance = FuelTracker(main_window)
    
    # Start the Tkinter event loop (keeps the window open)
    main_window.mainloop()