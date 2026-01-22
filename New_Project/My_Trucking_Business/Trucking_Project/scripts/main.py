# ---------------------------------------------------------------------------
# Date: 2026-01-11
# Script Name: main.py
# Author: omegazyph
# Updated: 2026-01-22
# Description: Modernized GUI for the Fuel Tracker. 
#              Uses improved spacing, color-coded results, and 
#              a cleaner layout for Windows 11 users.
# ---------------------------------------------------------------------------

import tkinter as tk
from tkinter import messagebox, ttk # Added ttk for more modern widgets
import os
from datetime import datetime
from fuel_logic import FuelDataManager

class FuelTrackerApp:
    def __init__(self, root_window):
        """ Initialize the modern interface and data connection. """
        self.root = root_window
        self.root.title("omegazyph | Fuel Performance Dashboard")
        self.root.geometry("650x950")
        self.root.configure(bg="#ffffff") # Clean white background

        # Establish connection to the logic file
        script_directory = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_directory)
        csv_full_path = os.path.join(project_root, "data", "fuel_history.csv")
        self.data_manager = FuelDataManager(csv_full_path)

        self.calculation_results = {"miles": 0.0, "mpg": 0.0, "cpm": 0.0}

        self.initialize_modern_ui()

    def initialize_modern_ui(self):
        """ Builds a visually appealing dashboard layout. """
        
        # --- HEADER SECTION ---
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=100)
        header_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(header_frame, text="FUEL TRACKER PRO", font=("Segoe UI", 22, "bold"), 
                 bg="#2c3e50", fg="#ecf0f1").pack(pady=25)

        # --- INPUT SECTION ---
        input_group = tk.LabelFrame(self.root, text=" Load Details ", font=("Segoe UI", 12, "bold"),
                                   bg="#ffffff", padx=20, pady=20, fg="#34495e")
        input_group.pack(padx=30, fill="x")

        # Define styles for reuse
        lbl_cfg = {"bg": "#ffffff", "font": ("Segoe UI", 10), "fg": "#7f8c8d"}
        
        # Grid layout for inputs
        self.entry_date = self.add_styled_entry(input_group, "Date:", 0)
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        self.entry_load = self.add_styled_entry(input_group, "Load ID:", 1)
        self.entry_start = self.add_styled_entry(input_group, "Start Odo:", 2)
        self.entry_end = self.add_styled_entry(input_group, "End Odo:", 3)
        self.entry_gallons = self.add_styled_entry(input_group, "Gallons:", 4)
        self.entry_cost = self.add_styled_entry(input_group, "Total Cost ($):", 5)

        # --- BUTTONS SECTION ---
        btn_container = tk.Frame(self.root, bg="#ffffff")
        btn_container.pack(pady=20)

        # Main Action Buttons
        tk.Button(btn_container, text="CALCULATE", command=self.perform_math, 
                  bg="#3498db", fg="white", font=("Segoe UI", 11, "bold"), 
                  width=18, bd=0, cursor="hand2").grid(row=0, column=0, padx=10)
        
        tk.Button(btn_container, text="CLEAR", command=self.clear_entries, 
                  bg="#95a5a6", fg="white", font=("Segoe UI", 11, "bold"), 
                  width=10, bd=0, cursor="hand2").grid(row=0, column=1, padx=10)

        # --- RESULTS CARD ---
        results_card = tk.Frame(self.root, bg="#f8f9fa", bd=1, relief="solid")
        results_card.pack(padx=30, pady=10, fill="x")

        self.label_miles = tk.Label(results_card, text="Total Miles: --", font=("Segoe UI", 12), bg="#f8f9fa")
        self.label_miles.pack(pady=5)
        
        self.label_mpg = tk.Label(results_card, text="MPG: --", font=("Segoe UI", 16, "bold"), 
                                  bg="#f8f9fa", fg="#27ae60")
        self.label_mpg.pack(pady=5)
        
        self.label_cpm = tk.Label(results_card, text="Cost Per Mile: --", font=("Segoe UI", 12), bg="#f8f9fa")
        self.label_cpm.pack(pady=5)

        # --- FINAL ACTIONS ---
        self.button_save = tk.Button(self.root, text="SAVE RECORD TO CSV", command=self.save_data, 
                                     bg="#27ae60", fg="white", font=("Segoe UI", 12, "bold"), 
                                     width=40, state="disabled", bd=0, cursor="hand2")
        self.button_save.pack(pady=20)

        tk.Button(self.root, text="Undo Last Entry", command=self.undo_last_save, 
                  bg="#ffffff", fg="#e74c3c", font=("Segoe UI", 9, "underline"), 
                  bd=0, cursor="hand2").pack()

    def add_styled_entry(self, parent, label_text, row_idx):
        """ Helper to create a clean-looking label and entry pair. """
        tk.Label(parent, text=label_text, bg="#ffffff", font=("Segoe UI", 10, "bold"), 
                 fg="#2c3e50").grid(row=row_idx, column=0, sticky="w", pady=8)
        
        # Using a Frame to simulate a border around the entry
        border_frame = tk.Frame(parent, bg="#bdc3c7", bd=1)
        border_frame.grid(row=row_idx, column=1, sticky="ew", padx=15)
        
        new_entry = tk.Entry(border_frame, font=("Segoe UI", 12), width=25, bd=0)
        new_entry.pack(padx=1, pady=1)
        return new_entry

    def perform_math(self):
        """ Reads input, performs calculations, and updates the UI colors. """
        try:
            start = float(self.entry_start.get())
            end = float(self.entry_end.get())
            gals = float(self.entry_gallons.get())
            cost = float(self.entry_cost.get())

            miles = end - start
            if miles <= 0:
                messagebox.showwarning("Mileage Error", "End odometer must be higher than start.")
                return

            mpg = miles / gals if gals > 0 else 0
            cpm = cost / miles if miles > 0 else 0

            self.calculation_results = {"miles": miles, "mpg": mpg, "cpm": cpm}

            # Update UI with formatted results
            self.label_miles.config(text=f"Total Trip Distance: {miles:,.1f} Miles")
            self.label_mpg.config(text=f"Efficiency: {mpg:.2f} MPG")
            self.label_cpm.config(text=f"Cost: ${cpm:.3f} per mile")
            
            self.button_save.config(state="normal", bg="#2ecc71") # Brighten green when active
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers in all performance fields.")

    def save_data(self):
        """ Package the data and send to the logic manager. """
        data = [
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
        self.data_manager.save_and_sort_data(data)
        messagebox.showinfo("Success", "Log entry saved and sorted.")
        self.button_save.config(state="disabled", bg="#95a5a6")

    def undo_last_save(self):
        """ Triggers the delete function from fuel_logic.py. """
        if messagebox.askyesno("Confirm Delete", "Remove the last saved entry?"):
            success, msg = self.data_manager.delete_last_saved_entry()
            messagebox.showinfo("Status", msg)

    def clear_entries(self):
        """ Reset the form for the next entry. """
        for e in [self.entry_load, self.entry_start, self.entry_end, self.entry_gallons, self.entry_cost]:
            e.delete(0, tk.END)
        self.button_save.config(state="disabled", bg="#95a5a6")

if __name__ == "__main__":
    app_root = tk.Tk()
    # Apply a standard theme if available
    style = ttk.Style(app_root)
    style.theme_use('clam')
    
    app_instance = FuelTrackerApp(app_root)
    app_root.mainloop()