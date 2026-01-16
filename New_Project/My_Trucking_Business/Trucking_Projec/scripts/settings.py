# ---------------------------------------------------------------------------
# Date: 2026-01-15
# Script Name: settings.py
# Author: omegazyph
# Updated: 2026-01-16
# Description: Manages both the fixed expenses JSON and the carrier 
#              configuration (Fee %) JSON.
# ---------------------------------------------------------------------------

import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os

def get_path(filename):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_dir, "data", filename)

def load_json(filename):
    path = get_path(filename)
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Default values if files are missing
        if filename == "config.json": return {"carrier_fee_percent": 25.0}
        return {}

def save_json(filename, data):
    path = get_path(filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def open_settings_window(parent_callback):
    exp_data = load_json("expenses.json")
    config_data = load_json("config.json")
    
    settings_win = tk.Toplevel()
    settings_win.title("Global Settings")
    settings_win.geometry("400x550")

    # --- Carrier Fee Section ---
    tk.Label(settings_win, text="Carrier Configuration", font=("Segoe UI", 11, "bold")).pack(pady=10)
    fee_frame = tk.Frame(settings_win)
    fee_frame.pack()
    
    tk.Label(fee_frame, text="Carrier Fee %:").grid(row=0, column=0)
    fee_var = tk.StringVar(value=str(config_data.get("carrier_fee_percent", 25.0)))
    fee_entry = tk.Entry(fee_frame, textvariable=fee_var, width=10)
    fee_entry.grid(row=0, column=1, padx=5)

    def save_config():
        try:
            val = float(fee_var.get())
            config_data["carrier_fee_percent"] = val
            save_json("config.json", config_data)
            messagebox.showinfo("Success", "Carrier fee updated!")
            parent_callback()
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number for the fee.")

    tk.Button(settings_win, text="Update Fee", command=save_config, bg="#3498db", fg="white").pack(pady=5)

    tk.Canvas(settings_win, height=2, bg="#ddd", highlightthickness=0).pack(fill="x", pady=10)

    # --- Fixed Expenses Section ---
    tk.Label(settings_win, text="Monthly Fixed Expenses", font=("Segoe UI", 11, "bold")).pack(pady=5)
    listbox = tk.Listbox(settings_win, width=45, height=10)
    listbox.pack(pady=5, padx=10)

    def refresh_list():
        listbox.delete(0, tk.END)
        for k, v in exp_data.items():
            listbox.insert(tk.END, f"{k}: ${v:,.2f}")
        parent_callback()

    def add_item():
        key = simpledialog.askstring("Input", "Expense Name:")
        if key:
            val = simpledialog.askfloat("Input", f"Monthly cost for {key}:")
            if val is not None:
                exp_data[key.lower()] = val
                save_json("expenses.json", exp_data)
                refresh_list()

    def delete_item():
        selection = listbox.curselection()
        if selection:
            item_text = listbox.get(selection[0])
            key = item_text.split(":")[0]
            del exp_data[key]
            save_json("expenses.json", exp_data)
            refresh_list()

    btn_frame = tk.Frame(settings_win)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Add Expense", command=add_item, bg="#27ae60", fg="white", width=12).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Delete", command=delete_item, bg="#e74c3c", fg="white", width=12).grid(row=0, column=1, padx=5)

    refresh_list()