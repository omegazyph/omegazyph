# ---------------------------------------------------------------------------
# Date: 2026-01-15
# Script Name: settings.py
# Author: omegazyph
# Updated: 2026-01-15
# Description: Logic for loading and editing the permanent expenses.json file.
# ---------------------------------------------------------------------------

import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os

def get_json_path():
    """Builds path to the JSON file in the data folder."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_dir, "data", "expenses.json")

def load_json():
    """Loads dictionary data from the permanent JSON file."""
    path = get_json_path()
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_json(data):
    """Saves dictionary data to the permanent JSON file."""
    path = get_json_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def open_settings_window(parent_callback):
    """GUI window to edit the permanent dictionary."""
    data = load_json()
    
    settings_win = tk.Toplevel()
    settings_win.title("Fixed Cost Manager")
    settings_win.geometry("350x450")

    tk.Label(settings_win, text="Manage Fixed Costs", font=("Arial", 12, "bold")).pack(pady=10)

    listbox = tk.Listbox(settings_win, width=40, height=15)
    listbox.pack(pady=5, padx=10)

    def refresh_list():
        listbox.delete(0, tk.END)
        for k, v in data.items():
            listbox.insert(tk.END, f"{k}: ${v:,.2f}")
        parent_callback() # Updates main.py total display

    def add_item():
        key = simpledialog.askstring("Input", "Expense Name:")
        if key:
            val = simpledialog.askfloat("Input", f"Monthly cost for {key}:")
            if val is not None:
                data[key.lower()] = val
                save_json(data)
                refresh_list()

    def delete_item():
        selection = listbox.curselection()
        if selection:
            item_text = listbox.get(selection[0])
            key = item_text.split(":")[0]
            del data[key]
            save_json(data)
            refresh_list()

    tk.Button(settings_win, text="Add New", command=add_item, bg="#27ae60", fg="white").pack(side="left", padx=20, pady=10)
    tk.Button(settings_win, text="Delete", command=delete_item, bg="#e74c3c", fg="white").pack(side="right", padx=20, pady=10)

    refresh_list()