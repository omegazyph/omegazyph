# ---------------------------------------------------------------------------
# Date: 2026-01-11
# Script Name: main.py
# Author: omegazyph
# Updated: 2026-01-22
# Description: Advanced Fuel Tracker. 
#              Calculates both Load MPG (overall) and Tank MPG (per fill-up).
# ---------------------------------------------------------------------------

import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime
from fuel_logic import FuelDataManager

class FuelTrackerApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("omegazyph | Load & Tank Optimizer")
        self.root.geometry("750x980")
        self.root.configure(bg="#ffffff")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(os.path.dirname(script_dir), "data", "fuel_history.csv")
        self.data_manager = FuelDataManager(csv_path)

        # Storage for current load
        self.fuel_purchases = [] 
        self.tank_performance_strings = [] # For saving to CSV
        self.calculation_results = {"miles": 0.0, "mpg": 0.0, "cpm": 0.0, "gals": 0.0, "cost": 0.0}

        self.initialize_ui()

    def initialize_ui(self):
        # HEADER
        header = tk.Frame(self.root, bg="#2c3e50")
        header.pack(fill="x", pady=(0, 10))
        tk.Label(header, text="LOAD & TANK PERFORMANCE", font=("Segoe UI", 18, "bold"), bg="#2c3e50", fg="#ecf0f1").pack(pady=20)

        # TRIP DETAILS
        trip_group = tk.LabelFrame(self.root, text=" 1. Load Odometer Range ", bg="#ffffff", padx=10, pady=10)
        trip_group.pack(padx=20, fill="x")
        self.ent_date = self.add_styled_entry(trip_group, "Date:", 0)
        self.ent_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.ent_load = self.add_styled_entry(trip_group, "Load ID:", 1)
        self.ent_start = self.add_styled_entry(trip_group, "Start of Load Odo:", 2)
        self.ent_end = self.add_styled_entry(trip_group, "End of Load Odo:", 3)

        # TANK DETAILS
        fuel_group = tk.LabelFrame(self.root, text=" 2. Individual Tank Fill-ups ", bg="#ffffff", padx=10, pady=10)
        fuel_group.pack(padx=20, pady=10, fill="x")
        self.ent_gals = self.add_styled_entry(fuel_group, "Gallons:", 0)
        self.ent_cost = self.add_styled_entry(fuel_group, "Cost ($):", 1)
        self.ent_tank_odo = self.add_styled_entry(fuel_group, "Odo at this Fill-up:", 2)

        tk.Button(fuel_group, text="+ Add Tank Receipt", command=self.add_tank_receipt, bg="#3498db", fg="white", font=("Segoe UI", 9, "bold")).grid(row=3, column=1, sticky="e", pady=5)

        self.fuel_listbox = tk.Listbox(fuel_group, height=4, font=("Segoe UI", 9))
        self.fuel_listbox.grid(row=4, column=0, columnspan=2, sticky="ew", pady=5)

        # ACTIONS
        btn_frame = tk.Frame(self.root, bg="#ffffff")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="CALCULATE PERFORMANCE", command=self.calculate, bg="#2c3e50", fg="white", width=25).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="CLEAR", command=self.reset, bg="#95a5a6", fg="white", width=10).grid(row=0, column=1, padx=5)

        self.res_label = tk.Label(self.root, text="Summary will appear here...", font=("Segoe UI", 10), bg="#ffffff", justify="left")
        self.res_label.pack(pady=10)

        self.btn_save = tk.Button(self.root, text="SAVE LOAD TO CSV", command=self.save, bg="#27ae60", fg="white", font=("Segoe UI", 12, "bold"), width=40, state="disabled")
        self.btn_save.pack(pady=10)

    def add_styled_entry(self, parent, label, row):
        tk.Label(parent, text=label, bg="#ffffff", font=("Segoe UI", 10, "bold")).grid(row=row, column=0, sticky="w")
        e = tk.Entry(parent, font=("Segoe UI", 11), bd=1, relief="solid")
        e.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
        return e

    def add_tank_receipt(self):
        """ Calculates MPG for just this tank before adding it to the load list. """
        try:
            gals = float(self.ent_gals.get())
            cost = float(self.ent_cost.get())
            current_odo = float(self.ent_tank_odo.get())
            
            # Figure out distance since last fill-up (or start of load)
            if not self.fuel_purchases:
                prev_odo = float(self.ent_start.get())
            else:
                prev_odo = self.fuel_purchases[-1][2] # The odo from the last receipt added

            tank_miles = current_odo - prev_odo
            
            if tank_miles <= 0:
                messagebox.showerror("Error", "Odo must be higher than previous stop.")
                return

            tank_mpg = tank_miles / gals
            
            # Store it: (gallons, cost, odo_at_stop, tank_mpg)
            self.fuel_purchases.append((gals, cost, current_odo, tank_mpg))
            
            display = f"Tank: {tank_miles:.1f} mi | {gals} gal | MPG: {tank_mpg:.2f}"
            self.fuel_listbox.insert(tk.END, display)
            self.tank_performance_strings.append(f"[{tank_mpg:.2f} MPG]")

            self.ent_gals.delete(0, tk.END)
            self.ent_cost.delete(0, tk.END)
            self.ent_tank_odo.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Fill in Gallons, Cost, and Odo for this tank.")

    def calculate(self):
        try:
            if not self.fuel_purchases:
                return

            total_gals = sum(f[0] for f in self.fuel_purchases)
            total_cost = sum(f[1] for f in self.fuel_purchases)
            trip_miles = float(self.ent_end.get()) - float(self.ent_start.get())

            load_mpg = trip_miles / total_gals
            load_cpm = total_cost / trip_miles

            self.calculation_results = {"miles": trip_miles, "mpg": load_mpg, "cpm": load_cpm, "gals": total_gals, "cost": total_cost}
            
            summary = f"OVERALL LOAD: {trip_miles:.1f} mi | {load_mpg:.2f} MPG | ${load_cpm:.3f} CPM\n"
            summary += f"Individual Tanks: {' -> '.join(self.tank_performance_strings)}"
            
            self.res_label.config(text=summary, fg="#27ae60")
            self.btn_save.config(state="normal")
        except Exception:
            messagebox.showerror("Error", "Check load odometer entries.")

    def save(self):
        tank_summary = " | ".join(self.tank_performance_strings)
        data = [
            self.ent_date.get(), self.ent_load.get(), self.ent_start.get(), self.ent_end.get(),
            f"{self.calculation_results['miles']:.1f}", f"{self.calculation_results['gals']:.2f}",
            f"{self.calculation_results['cost']:.2f}", f"{self.calculation_results['mpg']:.2f}",
            f"{self.calculation_results['cpm']:.3f}", tank_summary
        ]
        self.data_manager.save_and_sort_data(data)
        messagebox.showinfo("Saved", "Load and Tank data recorded.")
        self.reset()

    def reset(self):
        for e in [self.ent_load, self.ent_start, self.ent_end, self.ent_gals, self.ent_cost, self.ent_tank_odo]:
            e.delete(0, tk.END)
        self.fuel_purchases = []
        self.tank_performance_strings = []
        self.fuel_listbox.delete(0, tk.END)
        self.btn_save.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = FuelTrackerApp(root)
    root.mainloop()