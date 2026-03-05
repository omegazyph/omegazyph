###############################################################################
# Date: 2024-04-15
# Script Name: 2024-04-15_employee_lookup.py
# Autho---: omegazyph
# Updated: 2026-01-08
# Description: Reads employee data from a CSV file and prints a formatted 
#              list of names and phone numbers to the terminal.
###############################################################################

import csv
import os

# Define the relative path to your employee data
file_path = 'Code Academy Projects/Exam_coding/CSV_reading/employees.csv'

def run_employee_import():
    # Verify if the file exists before attempting to open
    if not os.path.exists(file_path):
        print(f"[!] Error: The file at {file_path} was not found.")
        return

    print(f"[*] Accessing Database: {file_path}\n")

    # Open the CSV file with newline='' as recommended by Python CSV docs
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        # DictReader uses the first row of the CSV as keys for a dictionary
        reader = csv.DictReader(csvfile)
        
        # Iterate through each row in the spreadsheet
        for row in reader:
            # Safely extract values; 'N/A' is the fallback if a column is missing
            name = row.get('Name', 'N/A')
            phone_number = row.get('Phone Number', 'N/A')
            
            # Print the formatted output to the VS Code terminal
            print(f"NAME: {name.ljust(15)} | TEL: {phone_number}")

    print("\n[*] Import Complete.")

if __name__ == "__main__":
    run_employee_import()