import json
import os
import subprocess
import tkinter as tkinter_gui
from tkinter import messagebox as gui_messagebox
from tkinter import ttk as gui_widgets

# Project Folder: Master_Expense_Tracker
# File Location: Master_Expense_Tracker/src/main_gui.py
# Date Created: May 19, 2026
# Date Updated: May 19, 2026
# Author: omegazyph
# Description: This program provides a Tkinter graphical user interface for the 
# Master Expense Tracker workspace. It loads dynamic settings from settings.json,
# displays calculations, and lets the user execute file synchronization scripts 
# with the click of a button.

class ExpenseTrackerApp:
    def __init__(self, window_root):
        self.window_root = window_root
        self.window_root.title("Omegazyph Master Expense Control Panel")
        self.window_root.geometry("650x500")
        
        # Setup paths based on standard project folder tree
        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        self.data_directory = os.path.abspath(os.path.join(self.script_directory, "..", "data"))
        self.settings_file_path = os.path.join(self.data_directory, "settings.json")
        
        # Initialize display labels
        self.status_label_text = tkinter_gui.StringVar(value="System Initialized. Ready for actions.")
        self.overhead_text = tkinter_gui.StringVar(value="$0.00")
        self.paid_text = tkinter_gui.StringVar(value="$0.00")
        self.balance_text = tkinter_gui.StringVar(value="$0.00")
        
        self.build_user_interface_widgets()
        self.load_and_display_metrics()

    def build_user_interface_widgets(self):
        """
        Creates frames, text regions, and button components inside the window frame.
        """
        # Header Label Title
        title_label = gui_widgets.Label(
            self.window_root, 
            text="Wayne's Expense & Ledger Dashboard", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=15)
        
        # --- FRAME 1: FINANCIAL SUMMARY METRICS DISPLAY ---
        summary_frame = gui_widgets.LabelFrame(self.window_root, text=" Calculated Database Summary ", padding=15)
        summary_frame.pack(fill="x", padx=20, pady=10)
        
        gui_widgets.Label(summary_frame, text="Base Monthly Overhead:", font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=5)
        gui_widgets.Label(summary_frame, textvariable=self.overhead_text, font=("Arial", 11, "bold"), foreground="blue").grid(row=0, column=1, sticky="w", padx=10)
        
        gui_widgets.Label(summary_frame, text="Total Rent Paid (All-Time):", font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=5)
        gui_widgets.Label(summary_frame, textvariable=self.paid_text, font=("Arial", 11, "bold"), foreground="green").grid(row=1, column=1, sticky="w", padx=10)
        
        gui_widgets.Label(summary_frame, text="Current Outstanding Rent:", font=("Arial", 11)).grid(row=2, column=0, sticky="w", pady=5)
        gui_widgets.Label(summary_frame, textvariable=self.balance_text, font=("Arial", 11, "bold"), foreground="red").grid(row=2, column=1, sticky="w", padx=10)

        # --- FRAME 2: AUTOMATION CONTROL BUTTONS ---
        control_frame = gui_widgets.LabelFrame(self.window_root, text=" Automation Control Scripts ", padding=15)
        control_frame.pack(fill="x", padx=20, pady=15)
        
        # Button 1: Run Converter
        run_converter_button = gui_widgets.Button(
            control_frame, 
            text="1. Run ODS to CSV Converter", 
            width=30, 
            command=self.execute_ods_converter_script
        )
        run_converter_button.pack(pady=5)
        
        # Button 2: Run Master Sync Ingestion
        run_sync_button = gui_widgets.Button(
            control_frame, 
            text="2. Sync CSV Data into Master JSON", 
            width=30, 
            command=self.execute_master_sync_script
        )
        run_sync_button.pack(pady=5)
        
        # Button 3: Refresh GUI Screen
        refresh_button = gui_widgets.Button(
            control_frame, 
            text="Refresh Dashboard Display", 
            width=30, 
            command=self.load_and_display_metrics
        )
        refresh_button.pack(pady=15)

        # --- FRAME 3: CONSOLE FOOTER STATUS BAR ---
        status_bar = gui_widgets.Label(
            self.window_root, 
            textvariable=self.status_label_text, 
            relief="sunken", 
            anchor="w", 
            padding=5
        )
        status_bar.pack(fill="x", side="bottom")

    def load_and_display_metrics(self):
        """
        Reads files off disk and updates text strings on screen to match values.
        """
        try:
            if not os.path.exists(self.settings_file_path):
                self.status_label_text.set("Error: settings.json file not found.")
                return
                
            with open(self.settings_file_path, "r") as f:
                settings_profile = json.load(f)
                
            path_rules = settings_profile.get("project_paths", {})
            master_json_filename = path_rules.get("master_ledger_filename", "expenses organized.json")
            full_master_json_path = os.path.join(self.data_directory, master_json_filename)
            
            if os.path.exists(full_master_json_path):
                with open(full_master_json_path, "r") as f:
                    master_database = json.load(f)
                
                # Pull metrics out of the JSON file data structures
                fixed_expenses = master_database.get("monthly_recurring_expenses", [])
                base_monthly_total = sum(item.get("amount_dollars", 0.0) for item in fixed_expenses)
                
                summary_data = master_database.get("financial_summary_metadata", {})
                all_time_paid = summary_data.get("total_rent_paid_all_time_dollars", 0.0)
                outstanding_balance = summary_data.get("total_rent_balance_remaining_dollars", 0.0)
                
                # Format text displays
                self.overhead_text.set(f"${base_monthly_total:,.2f}")
                self.paid_text.set(f"${all_time_paid:,.2f}")
                self.balance_text.set(f"${outstanding_balance:,.2f}")
                self.status_label_text.set("Dashboard interface updated from disk storage records.")
            else:
                self.status_label_text.set("Ready: Please run sync script to build database ledger.")
                
        except Exception as execution_error:
            self.status_label_text.set(f"Error loading dashboard fields: {str(execution_error)}")

    def execute_ods_converter_script(self):
        """
        Launches the external convert_ods_to_csv.py file process.
        """
        converter_script_path = os.path.join(self.script_directory, "convert_ods_to_csv.py")
        if not os.path.exists(converter_script_path):
            gui_messagebox.showerror("Error", f"Could not find converter script at:\n{converter_script_path}")
            return
            
        try:
            self.status_label_text.set("Executing ODS file folder scan and extraction...")
            # Run the process safely using subprocess pipeline
            result = subprocess.run(["python", converter_script_path], capture_output=True, text=True, check=True)
            self.status_label_text.set("CSV Converter script executed successfully.")
            gui_messagebox.showinfo("Success", "ODS files processed into unified flat CSV text file!")
        except subprocess.CalledProcessError as sub_error:
            gui_messagebox.showerror("Execution Error", f"Script crashed:\n{sub_error.stderr}")
            self.status_label_text.set("Converter script execution failure.")

    def execute_master_sync_script(self):
        """
        Launches the external update_master_ledger.py file process.
        """
        sync_script_path = os.path.join(self.script_directory, "update_master_ledger.py")
        if not os.path.exists(sync_script_path):
            gui_messagebox.showerror("Error", f"Could not find synchronization script at:\n{sync_script_path}")
            return
            
        try:
            self.status_label_text.set("Synchronizing CSV line items into master file database...")
            subprocess.run(["python", sync_script_path], capture_output=True, text=True, check=True)
            self.status_label_text.set("Master database synced successfully.")
            # Automatically reload the display frames to mirror new balances
            self.load_and_display_metrics()
            gui_messagebox.showinfo("Success", "Master JSON database ledger updated and reloaded!")
        except subprocess.CalledProcessError as sub_error:
            gui_messagebox.showerror("Execution Error", f"Script crashed:\n{sub_error.stderr}")
            self.status_label_text.set("Master synchronization pipeline failed.")

def main():
    window_instantiation = tkinter_gui.Tk()
    application_instance = ExpenseTrackerApp(window_root=window_instantiation)
    window_instantiation.mainloop()

if __name__ == "__main__":
    main()