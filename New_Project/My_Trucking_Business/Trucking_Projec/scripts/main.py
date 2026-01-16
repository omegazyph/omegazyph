# ---------------------------------------------------------------------------
# Date: 2026-01-15
# Script Name: main.py
# Author: omegazyph
# Updated: 2026-01-16
# Description: Main Trucking Calculator. Pulls Carrier Fee from config.json.
# ---------------------------------------------------------------------------

import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime
import settings 

class TruckApp:
    def __init__(self, root):
        self.root = root
        self.root.title("omegazyph's Mileage & Settlement Pro")
        self.root.geometry("500x920")
        self.root.configure(bg="#f4f4f4")

        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.trips_dir = os.path.join(self.base_dir, "data", "trips")

        self.footer_var = tk.StringVar()
        self.result_var = tk.StringVar(value="Waiting for calculation...")
        self.report_content = "" 
        self.target_file = ""    

        self.setup_ui()
        self.update_displays()

        self.root.bind('<Return>', lambda event: self.do_math())

    def update_displays(self):
        """Loads both expenses and the carrier fee from JSON files."""
        exp_data = settings.load_json("expenses.json")
        conf_data = settings.load_json("config.json")
        
        monthly_total = sum(exp_data.values())
        daily_rate = monthly_total / 30
        fee_pct = conf_data.get("carrier_fee_percent", 25.0)
        
        self.footer_var.set(f"Fee: {fee_pct}% | Monthly: ${monthly_total:,.2f} | Daily: ${daily_rate:,.2f}")

    def setup_ui(self):
        style = {"bg": "#f4f4f4", "font": ("Segoe UI", 10, "bold")}
        tk.Label(self.root, text="SETTLEMENT CALCULATOR", font=("Segoe UI", 16, "bold"), bg="#f4f4f4").pack(pady=15)

        in_frame = tk.Frame(self.root, bg="#f4f4f4")
        in_frame.pack(pady=5)

        def create_field(label, row):
            tk.Label(in_frame, text=label, **style).grid(row=row, column=0, sticky="e", pady=5)
            ent = tk.Entry(in_frame, font=("Segoe UI", 10), width=20)
            ent.grid(row=row, column=1, padx=10)
            return ent

        self.ent_trip = create_field("Trip/Settlement #:", 0)
        self.ent_income = create_field("Load Gross Rate ($):", 1) 
        self.ent_days = create_field("Days in Settlement:", 2) 
        self.ent_start = create_field("Start Odometer:", 3)
        self.ent_end = create_field("End Odometer:", 4)
        self.ent_gal = create_field("Gallons Pumped:", 5)
        self.ent_cost = create_field("Total Fuel Cost ($):", 6)
        
        self.ent_trip.focus_set()

        btn_frame = tk.Frame(self.root, bg="#f4f4f4")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="CALCULATE", command=self.do_math, bg="#2980b9", fg="white", font=style["font"], width=12).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="CLEAR", command=self.clear_all, bg="#95a5a6", fg="white", font=style["font"], width=12).grid(row=0, column=1, padx=5)

        tk.Label(self.root, textvariable=self.result_var, font=("Consolas", 10), bg="white", relief="sunken", width=55, height=22, padx=10, pady=10, justify="left").pack(pady=10)

        self.btn_save = tk.Button(self.root, text="SAVE SETTLEMENT REPORT", command=self.save_to_txt, bg="#27ae60", fg="white", font=style["font"], width=25, state="disabled")
        self.btn_save.pack(pady=5)

        tk.Button(self.root, text="Edit Settings & Expenses", command=lambda: settings.open_settings_window(self.update_displays)).pack(pady=10)
        tk.Label(self.root, textvariable=self.footer_var, font=("Segoe UI", 9, "italic"), bg="#f4f4f4", fg="#555").pack(side="bottom", pady=10)

    def do_math(self):
        try:
            exp_data = settings.load_json("expenses.json")
            conf_data = settings.load_json("config.json")
            
            monthly_total = sum(exp_data.values())
            daily_rate = monthly_total / 30
            fee_decimal = conf_data.get("carrier_fee_percent", 25.0) / 100

            t_num = self.ent_trip.get().strip()
            load_gross = float(self.ent_income.get())
            days = float(self.ent_days.get())
            start = float(self.ent_start.get())
            end = float(self.ent_end.get())
            gals = float(self.ent_gal.get())
            fuel_cost = float(self.ent_cost.get())

            dist = end - start
            if dist <= 0:
                messagebox.showwarning("Logic Error", "Check Odometer readings.")
                return

            carrier_fee = load_gross * fee_decimal
            adjusted_gross = load_gross - carrier_fee
            prorated_fixed = daily_rate * days
            total_expenses = fuel_cost + prorated_fixed
            net_profit = adjusted_gross - total_expenses
            
            mpg = dist / gals if gals > 0 else 0

            self.target_file = f"Trip_{t_num}.txt"
            self.report_content = (
                f"RECORD: SETTLEMENT {t_num}\n"
                f"DATE:   {datetime.now().strftime('%Y-%m-%d')}\n"
                f"{'='*45}\n"
                f"LOAD GROSS RATE:  ${load_gross:,.2f}\n"
                f"CARRIER FEE ({fee_decimal*100:.1f}%):-${carrier_fee:,.2f}\n"
                f"{'-'*45}\n"
                f"ADJUSTED GROSS:   ${adjusted_gross:,.2f}\n"
                f"{'='*45}\n"
                f"FUEL EXPENSE:     ${fuel_cost:,.2f}\n"
                f"FIXED DEDUCTIONS: ${prorated_fixed:,.2f} ({days} days)\n"
                f"TOTAL TRIP COSTS: ${total_expenses:,.2f}\n"
                f"{'='*45}\n"
                f"NET PROFIT:       ${net_profit:,.2f}\n"
                f"{'='*45}\n"
                f"DISTANCE:         {dist:,.1f} Miles\n"
                f"FUEL ECONOMY:     {mpg:.2f} MPG\n"
            )
            self.result_var.set(self.report_content)
            self.btn_save.config(state="normal")
        except ValueError:
            messagebox.showerror("Error", "Check your numbers.")

    def save_to_txt(self):
        os.makedirs(self.trips_dir, exist_ok=True)
        path = os.path.join(self.trips_dir, self.target_file)
        with open(path, "w") as f: f.write(self.report_content)
        messagebox.showinfo("Saved", f"Settlement {self.target_file} saved.")
        self.btn_save.config(state="disabled")

    def clear_all(self):
        for entry in [self.ent_trip, self.ent_income, self.ent_days, self.ent_start, self.ent_end, self.ent_gal, self.ent_cost]:
            entry.delete(0, tk.END)
        self.result_var.set("Waiting...")
        self.btn_save.config(state="disabled")
        self.ent_trip.focus_set()

if __name__ == "__main__":
    root = tk.Tk()
    app = TruckApp(root)
    root.mainloop()