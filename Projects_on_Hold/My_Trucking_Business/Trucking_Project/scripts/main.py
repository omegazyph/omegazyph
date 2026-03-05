# ---------------------------------------------------------------------------
# Date: 2026-01-11
# Script Name: main.py
# Author: omegazyph
# Updated: 2026-01-22
# Description: Advanced Fuel Dashboard with Stats Trends (30/60/Life).
#              Full non-shorthand code for VSCode/Ruff compatibility.
# ---------------------------------------------------------------------------

import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime
from fuel_logic import FuelDataManager

class FuelTrackerApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("omegazyph | Business Performance Dashboard")
        self.root.geometry("750x1050")
        self.root.configure(bg="#ffffff")

        # Setup paths and data manager
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        csv_path = os.path.join(project_root, "data", "fuel_history.csv")
        self.data_manager = FuelDataManager(csv_path)

        # Temporary load memory
        self.fuel_purchases = [] 
        self.tank_summary_list = [] 
        self.calculation_results = {
            "miles": 0.0, "mpg": 0.0, "cpm": 0.0, "gals": 0.0, "cost": 0.0
        }

        self.initialize_ui()
        # Call the stats engine on startup to show current trends
        self.refresh_performance_stats()

    def initialize_ui(self):
        """ Builds the layout including the new Stats Bar. """
        # HEADER
        header_bar = tk.Frame(self.root, bg="#2c3e50")
        header_bar.pack(fill="x", pady=(0, 10))
        tk.Label(
            header_bar, text="FUEL PERFORMANCE DASHBOARD", 
            font=("Segoe UI", 18, "bold"), bg="#2c3e50", fg="#ecf0f1"
        ).pack(pady=20)

        # SECTION 1: LOAD INFO
        trip_box = tk.LabelFrame(self.root, text=" 1. Load Odometer ", bg="#ffffff", padx=10, pady=10)
        trip_box.pack(padx=20, fill="x")
        self.ent_date = self.add_styled_entry(trip_box, "Date:", 0)
        self.ent_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.ent_load = self.add_styled_entry(trip_box, "Load ID:", 1)
        self.ent_start = self.add_styled_entry(trip_box, "Start Odo:", 2)
        self.ent_end = self.add_styled_entry(trip_box, "End Odo:", 3)

        # SECTION 2: TANK ENTRIES
        fuel_box = tk.LabelFrame(self.root, text=" 2. Individual Tank Stops ", bg="#ffffff", padx=10, pady=10)
        fuel_box.pack(padx=20, pady=10, fill="x")
        self.ent_gals = self.add_styled_entry(fuel_box, "Gallons:", 0)
        self.ent_cost = self.add_styled_entry(fuel_box, "Cost ($):", 1)
        self.ent_tank_odo = self.add_styled_entry(fuel_box, "Odo at Pump:", 2)

        tk.Button(
            fuel_box, text="+ Add Tank Receipt", command=self.add_tank_receipt, 
            bg="#3498db", fg="white", font=("Segoe UI", 9, "bold")
        ).grid(row=3, column=1, sticky="e", pady=10)
        
        self.fuel_listbox = tk.Listbox(fuel_box, height=4, font=("Consolas", 10), bg="#f8f9fa")
        self.fuel_listbox.grid(row=4, column=0, columnspan=2, sticky="ew", pady=5)

        # SECTION 3: TRENDS (THE STATS ENGINE DISPLAY)
        stats_box = tk.LabelFrame(self.root, text=" Performance Trends (MPG) ", bg="#f1f2f6", padx=10, pady=10)
        stats_box.pack(padx=20, pady=10, fill="x")
        
        self.lbl_30 = tk.Label(stats_box, text="30-Day: --", font=("Segoe UI", 10, "bold"), bg="#f1f2f6")
        self.lbl_30.grid(row=0, column=0, padx=25)
        self.lbl_60 = tk.Label(stats_box, text="60-Day: --", font=("Segoe UI", 10, "bold"), bg="#f1f2f6")
        self.lbl_60.grid(row=0, column=1, padx=25)
        self.lbl_life = tk.Label(stats_box, text="Lifetime: --", font=("Segoe UI", 10, "bold"), bg="#f1f2f6")
        self.lbl_life.grid(row=0, column=2, padx=25)

        # FINAL ACTIONS
        action_bar = tk.Frame(self.root, bg="#ffffff")
        action_bar.pack(pady=10)
        tk.Button(action_bar, text="FINALIZE LOAD", command=self.calculate_load, 
                  bg="#2c3e50", fg="white", width=20).grid(row=0, column=0, padx=5)
        
        self.btn_save = tk.Button(self.root, text="SAVE LOAD TO HISTORY", command=self.save_load, 
                                  bg="#27ae60", fg="white", font=("Segoe UI", 12, "bold"), 
                                  width=40, state="disabled")
        self.btn_save.pack(pady=10)

    def refresh_performance_stats(self):
        """ Calls the stats engine and updates the trend labels. """
        avg30, avg60, avgLife = self.data_manager.get_stats()
        self.lbl_30.config(text=f"30-Day: {avg30}", fg="#2980b9")
        self.lbl_60.config(text=f"60-Day: {avg60}", fg="#2c3e50")
        self.lbl_life.config(text=f"Lifetime: {avgLife}", fg="#27ae60")

    def add_styled_entry(self, parent, label, row):
        tk.Label(parent, text=label, bg="#ffffff", font=("Segoe UI", 10, "bold")).grid(row=row, column=0, sticky="w")
        e = tk.Entry(parent, font=("Segoe UI", 11), bd=1, relief="solid")
        e.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
        return e

    def add_tank_receipt(self):
        """ Math for individual tanks and running averages. """
        try:
            gals = float(self.ent_gals.get())
            cost = float(self.ent_cost.get())
            c_odo = float(self.ent_tank_odo.get())
            s_odo = float(self.ent_start.get())
            
            p_odo = self.fuel_purchases[-1][2] if self.fuel_purchases else s_odo
            miles = c_odo - p_odo
            
            if miles <= 0:
                messagebox.showerror("Error", "Odo must be higher than previous.")
                return

            tank_mpg = miles / gals
            self.fuel_purchases.append((gals, cost, c_odo))
            
            total_g = sum(p[0] for p in self.fuel_purchases)
            run_avg = (c_odo - s_odo) / total_g
            
            self.fuel_listbox.insert(tk.END, f"Tank: {tank_mpg:.2f} | Running: {run_avg:.2f}")
            self.tank_summary_list.append(f"[{tank_mpg:.2f} R:{run_avg:.2f}]")
            
            # Clear inputs
            for entry in [self.ent_gals, self.ent_cost, self.ent_tank_odo]:
                entry.delete(0, tk.END)
        except Exception:
            messagebox.showerror("Error", "Check tank inputs.")

    def calculate_load(self):
        """ Final load totals before saving. """
        try:
            total_g = sum(p[0] for p in self.fuel_purchases)
            total_c = sum(p[1] for p in self.fuel_purchases)
            trip_m = float(self.ent_end.get()) - float(self.ent_start.get())
            
            self.calculation_results = {
                "miles": trip_m, "mpg": trip_m/total_g, 
                "cpm": total_c/trip_m, "gals": total_g, "cost": total_c
            }
            self.btn_save.config(state="normal")
        except Exception:
            messagebox.showerror("Error", "Enter Ending Odometer.")

    def save_load(self):
        """ Saves data and refreshes the trend bar. """
        summary = " | ".join(self.tank_summary_list)
        row = [
            self.ent_date.get(), self.ent_load.get(), self.ent_start.get(), self.ent_end.get(),
            f"{self.calculation_results['miles']:.1f}", f"{self.calculation_results['gals']:.2f}",
            f"{self.calculation_results['cost']:.2f}", f"{self.calculation_results['mpg']:.2f}",
            f"{self.calculation_results['cpm']:.3f}", summary
        ]
        self.data_manager.save_and_sort_data(row)
        self.refresh_performance_stats()
        self.reset_form()
        messagebox.showinfo("Success", "Load recorded.")

    def reset_form(self):
        for e in [self.ent_load, self.ent_start, self.ent_end, self.ent_gals, self.ent_cost, self.ent_tank_odo]:
            e.delete(0, tk.END)