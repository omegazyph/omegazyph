# ---------------------------------------------------------------------------
# Date: 2026-01-11
# Script Name: fuel_logic.py
# Author: omegazyph
# Updated: 2026-01-22
# Description: Handles CSV data management. Every statement is on its own line
#              to comply with clean-code standards and avoid Ruff errors.
# ---------------------------------------------------------------------------

import os
import csv

class FuelDataManager:
    def __init__(self, spreadsheet_file_path):
        """
        Initializes the file path and the standard header for the CSV file.
        """
        self.spreadsheet_file_path = spreadsheet_file_path
        self.data_directory = os.path.dirname(spreadsheet_file_path)
        self.header = [
            "Date", 
            "Load ID", 
            "Starting Miles", 
            "Ending Miles", 
            "Total Trip Miles", 
            "Gallons Used", 
            "Fuel Cost USD", 
            "MPG", 
            "Fuel CPM"
        ]

    def read_all_records(self):
        """
        Reads the CSV and returns the header and all data rows.
        No shorthand; every step is explicitly defined.
        """
        records = []
        if os.path.isfile(self.spreadsheet_file_path):
            with open(self.spreadsheet_file_path, mode='r', newline='') as csv_file:
                csv_reader = csv.reader(csv_file)
                # Capture header or use default if file is empty
                current_header = next(csv_reader, self.header)
                
                for row in csv_reader:
                    # Check if the row actually has data
                    if row:
                        records.append(row)
            
            return current_header, records
        
        # If file doesn't exist, return default header and empty list
        return self.header, []

    def save_and_sort_data(self, new_row_data):
        """
        Adds new data and performs a double-sort.
        """
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)

        header, all_entries = self.read_all_records()
        all_entries.append(new_row_data)

        # Sort Priority: 1st Load ID, 2nd Date
        all_entries.sort(key=lambda x: (x[1], x[0]))

        with open(self.spreadsheet_file_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)
            csv_writer.writerows(all_entries)

    def delete_last_saved_entry(self):
        """
        Removes the last row from the CSV file.
        Expanded if-statements to avoid 'multiple statements on one line' errors.
        """
        header, all_entries = self.read_all_records()
        
        if not all_entries:
            return False, "Spreadsheet is empty."
            
        # Remove the last record from the list
        all_entries.pop()
        
        with open(self.spreadsheet_file_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)
            csv_writer.writerows(all_entries)
            
        return True, "Last entry removed."