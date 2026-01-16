# ---------------------------------------------------------------------------
# Date: 2026-01-15
# Script Name: main.py
# Author: omegazyph
# Updated: 2026-01-15
# Description: Main Trucking Calculator. Calculates MPG and Cost-Per-Mile.
#              Saves individual readable reports named by Trip Number.
# ---------------------------------------------------------------------------

import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime
import settings  # Custom module for JSON handling

class TruckApp:
    def __init__(self, root):
        self.root = root
        self.root.title("omegazyph's Mileage Pro")
        self.root.geometry("460x720")
        self.root.configure(bg="#f4f4f4")

        # Define directory for saving trip reports
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.trips_dir = os.path.join(self.base_dir, "data", "trips")

        # State variables
        self.expense_total_var = tk.StringVar()
        self.result_var = tk.StringVar(value="Waiting for calculation...")
        self.report_content = "" 
        self.target_file = ""    

        self.setup_ui()
        self.update_expense_display()

        # Keyboard Binding: Enter key to calculate
        self.root.bind('<Return>', lambda event: self.do_math())

    def update_expense_display(self):
        """Updates the total fixed costs shown at the bottom."""
        data = settings.load_json()
        total = sum(data.values())
        self.expense_total_var.set(f"Fixed Costs Loaded: ${total:,.2f}")

    def setup_ui(self):
        """Builds the GUI layout and widgets."""
        style = {"bg": "#f4f4f4", "font": ("Segoe UI", 10, "bold")}
        
        tk.Label(self.root, text="TRUCK TRIP CALCULATOR", 
                 font=("Segoe UI", 16, "bold"), bg="#f4f4f4").pack(pady=15)

        # Input Group
        in_frame = tk.Frame(self.root, bg="#f4f4f4")
        in_frame.pack(pady=10)

        def create_field(label, row):
            tk.Label(in_frame, text=label, **style).grid(row=row, column=0, sticky="e", pady=5)
            ent = tk.Entry(in_frame, font=("Segoe UI", 10), width=20)
            ent.grid(row=row, column=1, padx=10)
            return ent

        self.ent_trip = create_field("Trip Number:", 0)
        self.ent_start = create_field("Start Odometer:", 1)
        self.ent_end = create_field("End Odometer:", 2)
        self.ent_gal = create_field("Gallons:", 3)
        self.ent_cost = create_field("Fuel Total ($):", 4)
        
        self.ent_trip.focus_set()

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#f4f4f4")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="CALCULATE", command=self.do_math, 
                  bg="#2980b9", fg="white", font=style["font"], width=12).grid(row=0, column=0, padx=5)
        
        tk.Button(btn_frame, text="CLEAR", command=self.clear_all, 
                  bg="#95a5a6", fg="white", font=style["font"], width=12).grid(row=0, column=1, padx=5)

        # Results Label
        tk.Label(self.root, textvariable=self.result_var, font=("Consolas", 10), bg="white", 
                 relief="sunken", width=45, height=12, padx=10, pady=10, justify="left").pack(pady=10)

        # Save Button
        self.btn_save = tk.Button(self.root, text="SAVE TRIP REPORT", command=self.save_to_txt, 
                                  bg="#27ae60", fg="white", font=style["font"], width=25, state="disabled")
        self.btn_save.pack(pady=5)

        # Settings Access
        tk.Button(self.root, text="Edit Expenses", 
                  command=lambda: settings.open_settings_window(self.update_expense_display)).pack(pady=10)
        
        # Bottom Cost Display
        tk.Label(self.root, textvariable=self.expense_total_var, 
                 font=("Segoe UI", 9, "italic"), bg="#f4f4f4", fg="#555").pack(side="bottom", pady=10)

    def do_math(self):
        """Performs calculation logic and formats the report."""
        try:
            data = settings.load_json()
            total_fixed = sum(data.values())

            t_num = self.ent_trip.get().strip()
            start = float(self.ent_start.get())
            end = float(self.ent_end.get())
            gals = float(self.ent_gal.get())
            fuel = float(self.ent_cost.get())

            if not t_num:
                messagebox.showwarning("Missing Data", "Please enter a Trip Number.")
                return

            dist = end - start
            if dist <= 0:
                messagebox.showwarning("Logic Error", "End miles must be > Start miles.")
                return

            mpg = dist / gals
            total_op_cost = fuel + total_fixed
            cpm = total_op_cost / dist

            self.target_file = f"Trip_{t_num}.txt"
            self.report_content = (
                f"RECORD: TRIP {t_num}\n"
                f"DATE:   {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                f"{'-'*35}\n"
                f"START MILES:    {start:,.1f}\n"
                f"END MILES:      {end:,.1f}\n"
                f"TOTAL DISTANCE: {dist:,.1f} Miles\n"
                f"FUEL USED:      {gals:,.2f} Gallons\n"
                f"AVG ECONOMY:    {mpg:.2f} MPG\n"
                f"{'-'*35}\n"
                f"FUEL COST:      ${fuel:,.2f}\n"
                f"FIXED EXPENSES: ${total_fixed:,.2f}\n"
                f"TOTAL TRIP EXP: ${total_op_cost:,.2f}\n"
                f"COST PER MILE:  ${cpm:.2f}\n"
                f"{'='*35}"
            )

            self.result_var.set(self.report_content)
            self.btn_save.config(state="normal")

        except ValueError:
            messagebox.showerror("Input Error", "Please use numbers for Odometer and Fuel.")

    def save_to_txt(self):
        """Writes the trip report to a unique text file."""
        os.makedirs(self.trips_dir, exist_ok=True)
        path = os.path.join(self.trips_dir, self.target_file)
        
        try:
            with open(path, "w") as f:
                f.write(self.report_content)
            messagebox.showinfo("Saved", f"Successfully saved to:\n{self.target_file}")
            self.btn_save.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

    def clear_all(self):
        """Clears all text fields and resets focus."""
        for entry in [self.ent_trip, self.ent_start, self.ent_end, self.ent_gal, self.ent_cost]:
            entry.delete(0, tk.END)
        self.result_var.set("Waiting for calculation...")
        self.btn_save.config(state="disabled")
        self.ent_trip.focus_set()

if __name__ == "__main__":
    root = tk.Tk()
    app = TruckApp(root)
    root.mainloop()