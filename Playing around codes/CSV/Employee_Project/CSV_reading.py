#!/usr/bin/env python3
"""
==============================================================================
SCRIPT NAME:    CSV_reading.py
DESCRIPTION:    A script to parse employee data from a CSV file. Updated with
                dynamic pathing for better folder organization.
AUTHOR:         Wayne Stock (omegazyph)
DATE CREATED:   2024-04-23
DATE UPDATED:   2026-01-05
VERSION:        1.3
==============================================================================
"""

import csv
import os

# Get the directory where THIS script is saved
# This ensures it finds the CSV even after you move the folder
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, 'employees.csv')

def main():
    """Main function to read and display CSV data."""
    
    if not os.path.exists(file_path):
        print(f"Error: Could not find 'employees.csv' in: {base_dir}")
        return

    print("============================================================================")
    print("                      OMEGAZYPH EMPLOYEE DIRECTORY")
    print("============================================================================\n")

    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            # quotechar handles the single quotes in your data
            reader = csv.DictReader(csvfile, quotechar="'", skipinitialspace=True)
            
            print(f"{'NAME':<15} | {'EMAIL':<25} | {'PHONE NUMBER'}")
            print("-" * 75)
            
            for row in reader:
                name = row.get('Name', 'N/A')
                email = row.get('Email', 'N/A')
                phone = row.get('Phone Number', 'N/A')
                print(f"{name:<15} | {email:<25} | {phone}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    print("\n" + "="*76)

if __name__ == "__main__":
    main()