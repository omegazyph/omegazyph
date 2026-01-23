# ---------------------------------------------------------------------------
# Date: 2026-01-11
# Script Name: fuel_logic.py
# Author: omegazyph
# Updated: 2026-01-22
# Description: Handles CSV data management. 
#              Updated to include 'Tank MPG' for individual fuel stops.
# ---------------------------------------------------------------------------

import os
import csv

class FuelDataManager:
    def __init__(self, spreadsheet_file_path):
        """
        Initializes the file path and the updated header for the CSV file.
        """
        self.spreadsheet_file_path = spreadsheet_file_path
        self.data_directory = os.path.dirname(spreadsheet_file_path)
        
        # Expanded header to include individual tank performance
        self.header = [
            "Date", 
            "Load ID", 
            "Starting Miles", 
            "Ending Miles", 
            "Total Trip Miles", 
            "Total Gallons", 
            "Total Cost", 
            "Load MPG", 
            "Load CPM",
            "Tank Breakdowns" # New column for individual tank stats
        ]

    def read_all_records(self):
        """
        Reads the CSV and returns the header and all data rows.
        """
        records = []
        if os.path.isfile(self.spreadsheet_file_path):
            with open(self.spreadsheet_file_path, mode='r', newline='') as csv_file:
                csv_reader = csv.reader(csv_file)
                current_header = next(csv_reader, self.header)
                
                for row in csv_reader:
                    if row:
                        records.append(row)
            
            return current_header, records
        
        return self.header, []

    def save_and_sort_data(self, new_row_data):
        """
        Adds new data and performs a double-sort by Load ID then Date.
        """
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)

        header, all_entries = self.read_all_records()
        all_entries.append(new_row_data)

        all_entries.sort(key=lambda x: (x[1], x[0]))

        with open(self.spreadsheet_file_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)
            csv_writer.writerows(all_entries)

    def delete_last_saved_entry(self):
        """
        Removes the last row from the CSV file.
        """
        header, all_entries = self.read_all_records()
        
        if not all_entries:
            return False, "Spreadsheet is empty."
            
        all_entries.pop()
        
        with open(self.spreadsheet_file_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)
            csv_writer.writerows(all_entries)
            
        return True, "Last entry removed."