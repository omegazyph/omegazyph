# ---------------------------------------------------------------------------
# Date: 2026-01-11
# Script Name: fuel_logic.py
# Author: omegazyph
# Updated: 2026-01-21
# Description: Logic and Data Handling for the Fuel Tracker.
#              Contains double-sorting logic: Load Number then Date.
# ---------------------------------------------------------------------------

import os
import csv

class FuelDataManager:
    def __init__(self, spreadsheet_file_path):
        self.spreadsheet_file_path = spreadsheet_file_path
        self.data_directory = os.path.dirname(spreadsheet_file_path)
        self.header = ["Date", "Load ID", "Starting Miles", "Ending Miles", 
                       "Total Trip Miles", "Gallons Used", "Fuel Cost USD", 
                       "MPG", "Fuel CPM"]

    def save_and_sort_data(self, new_row_data):
        """
        Saves data and performs a double-sort: 
        Primary Sort: Load Number (Index 1)
        Secondary Sort: Date (Index 0)
        """
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)

        all_entries = []
        
        # 1. Read existing data if the file exists
        if os.path.isfile(self.spreadsheet_file_path):
            with open(self.spreadsheet_file_path, mode='r', newline='') as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader) # Skip the header
                for row in csv_reader:
                    if row:
                        all_entries.append(row)

        # 2. Add the new entry
        all_entries.append(new_row_data)

        # 3. Double Sort: Sort by Load Number (Index 1), then Date (Index 0)
        # Using a tuple (x[1], x[0]) tells Python the priority of sorting.
        all_entries.sort(key=lambda x: (x[1], x[0]))

        # 4. Write back to file
        with open(self.spreadsheet_file_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(self.header)
            csv_writer.writerows(all_entries)