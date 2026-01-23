# ---------------------------------------------------------------------------
# Date: 2026-01-11
# Script Name: main.py
# Author: omegazyph
# Updated: 2026-01-22
# Description: Modern GUI with Multi-Fuel Entry Support. 
#              Full, non-shorthand code structure for maximum readability.
# ---------------------------------------------------------------------------

import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime
from fuel_logic import FuelDataManager

class FuelTrackerApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("omegazyph | Multi-Fuel Tracker")
        self.root.geometry("700x950")
        self.root.configure(bg="#ffffff")

        # Establish file pathing
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(script_dir)
        csv_path = os.path.join(project_dir, "data", "fuel_history.csv")
        
        self.data_manager = FuelDataManager(csv_path)

        # Storage for fuel and calculations
        self.fuel_purchases = [] 
        self.calculation_results = {
            "miles": 0.0, 
            "mpg": 0.0, 
            "cpm": 0.0, 
            "gals": 0.0, 
            "cost": 0.0
        }

        self.initialize_ui()

    def initialize_ui(self):
        """ Builds the layout with full widget definitions. """
        header = tk.Frame(self.root, bg="#2c3e50")
        header.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            header, 
            text="FUEL PERFORMANCE DASHBOARD", 
            font=("Segoe UI", 18, "bold"), 
            bg="#2c3e50", 
            fg="#ecf0f1"
        ).pack(pady=20)

        # Load and Mileage inputs
        main_input = tk.LabelFrame(self.root, text=" Trip Details ", bg="#ffffff", padx=10, pady=10)
        main_input.pack(padx=20, fill="x")

        self.ent_date = self.add_styled_entry(main_input, "Date:", 0)
        self.ent_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        self.ent_load = self.add_styled_entry(main_input, "Load ID:", 1)
        self.ent_start = self.add_styled_entry(main_input, "Start Odo:", 2)
        self.ent_end = self.add_styled_entry(main_input, "End Odo:", 3)

        # Fuel inputs
        fuel_input = tk.LabelFrame(self.root, text=" Fuel Purchases ", bg="#ffffff", padx=10, pady=10)
        fuel_input.pack(padx=20, pady=10, fill="x")

        self.ent_gals = self.add_styled_entry(fuel_input, "Gallons:", 0)
        self.ent_cost = self.add_styled_entry(fuel_input, "Cost ($):", 1)

        tk.Button(
            fuel_input, 
            text="+ Add Fuel Receipt", 
            command=self.add_fuel_receipt,
            bg="#3498db", 
            fg="white", 
            font=("Segoe UI", 9, "bold")
        ).grid(row=2, column=1, sticky="e", pady=5)

        self.fuel_listbox = tk.Listbox(fuel_input, height=3, font=("Segoe UI", 9))
        self.fuel_listbox.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)

        # Totals and Saving
        btn_frame = tk.Frame(self.root, bg="#ffffff")
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame, 
            text="CALCULATE TOTALS", 
            command=self.calculate, 
            bg="#2c3e50", 
            fg="white", 
            width=20
        ).grid(row=0, column=0, padx=5)
        
        tk.Button(
            btn_frame, 
            text="CLEAR ALL", 
            command=self.reset, 
            bg="#95a5a6", 
            fg="white", 
            width=10
        ).grid(row=0, column=1, padx=5)

        self.res_label = tk.Label(self.root, text="Ready for input...", font=("Segoe UI", 11), bg="#ffffff")
        self.res_label.pack(pady=10)

        self.btn_save = tk.Button(
            self.root, 
            text="SAVE LOAD TO SPREADSHEET", 
            command=self.save, 
            bg="#27ae60", 
            fg="white", 
            font=("Segoe UI", 12, "bold"), 
            width=40, 
            state="disabled"
        )
        self.btn_save.pack(pady=10)

    def add_styled_entry(self, parent, label, row):
        """ Creates a full label and entry pair. """
        tk.Label(parent, text=label, bg="#ffffff", font=("Segoe UI", 10, "bold")).grid(row=row, column=0, sticky="w")
        entry_widget = tk.Entry(parent, font=("Segoe UI", 11), bd=1, relief="solid")
        entry_widget.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
        return entry_widget

    def add_fuel_receipt(self):
        """ Explicitly adds fuel stop to list. """
        try:
            gallons_value = float(self.ent_gals.get())
            cost_value = float(self.ent_cost.get())
            
            # Append as a tuple to our list
            self.fuel_purchases.append((gallons_value, cost_value))
            
            # Update the visual list
            display_text = f"Added: {gallons_value} Gallons for ${cost_value}"
            self.fuel_listbox.insert(tk.END, display_text)
            
            # Clear the fuel input boxes
            self.ent_gals.delete(0, tk.END)
            self.ent_cost.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Enter numeric values for fuel gallons and cost.")

    def calculate(self):
        """ Calculates trip performance without shorthand logic. """
        try:
            if not self.fuel_purchases:
                messagebox.showwarning("Warning", "Please add at least one fuel purchase receipt.")
                return

            # Sum up all recorded fuel
            total_gals = 0.0
            total_cost = 0.0
            for gallons, cost in self.fuel_purchases:
                total_gals = total_gals + gallons
                total_cost = total_cost + cost

            # Calculate mileage
            start_miles = float(self.ent_start.get())
            end_miles = float(self.ent_end.get())
            trip_miles = end_miles - start_miles

            if trip_miles <= 0:
                messagebox.showerror("Error", "Ending odometer reading must be higher than start.")
                return

            # Perform MPG and CPM math
            mpg_value = trip_miles / total_gals
            cpm_value = total_cost / trip_miles

            # Update storage dictionary
            self.calculation_results["miles"] = trip_miles
            self.calculation_results["mpg"] = mpg_value
            self.calculation_results["cpm"] = cpm_value
            self.calculation_results["gals"] = total_gals
            self.calculation_results["cost"] = total_cost
            
            # Update display
            result_summary = f"Total Miles: {trip_miles:.1f} | Total Gals: {total_gals:.2f}\n"
            result_summary += f"MPG: {mpg_value:.2f} | CPM: ${cpm_value:.3f}"
            
            self.res_label.config(text=result_summary, fg="#27ae60")
            self.btn_save.config(state="normal")
            
        except ValueError:
            messagebox.showerror("Error", "Ensure all odometer readings are numbers.")

    def save(self):
        """ Packages data and calls logic manager. """
        formatted_data = [
            self.ent_date.get(), 
            self.ent_load.get(), 
            self.ent_start.get(), 
            self.ent_end.get(),
            f"{self.calculation_results['miles']:.1f}", 
            f"{self.calculation_results['gals']:.2f}",
            f"{self.calculation_results['cost']:.2f}", 
            f"{self.calculation_results['mpg']:.2f}",
            f"{self.calculation_results['cpm']:.3f}"
        ]
        
        self.data_manager.save_and_sort_data(formatted_data)
        messagebox.showinfo("Saved", "Load data saved and sorted.")
        self.reset()

    def reset(self):
        """ Fully resets the application state. """
        self.ent_load.delete(0, tk.END)
        self.ent_start.delete(0, tk.END)
        self.ent_end.delete(0, tk.END)
        self.ent_gals.delete(0, tk.END)
        self.ent_cost.delete(0, tk.END)
        
        self.fuel_purchases = []
        self.fuel_listbox.delete(0, tk.END)
        self.btn_save.config(state="disabled")
        self.res_label.config(text="Form reset.", fg="black")

if __name__ == "__main__":
    main_window = tk.Tk()
    app = FuelTrackerApp(main_window)
    main_window.mainloop()