# ---------------------------------------------------------------------------
# Date: 2026-01-11
# Script Name: fuel_logic.py
# Author: omegazyph
# Updated: 2026-01-22
# Description: Handles CSV data and contains the Stats Engine for 
#              calculating 30/60/Lifetime performance metrics.
# ---------------------------------------------------------------------------

import os
import csv
from datetime import datetime, timedelta

class FuelDataManager:
    def __init__(self, spreadsheet_file_path):
        """ Initializes the data path and the standard CSV structure. """
        self.spreadsheet_file_path = spreadsheet_file_path
        self.data_directory = os.path.dirname(spreadsheet_file_path)
        self.header = [
            "Date", "Load ID", "Starting Miles", "Ending Miles", 
            "Total Trip Miles", "Total Gallons", "Total Cost", 
            "Load MPG", "Load CPM", "Tank Breakdowns"
        ]

    def read_all_records(self):
        """ Reads the CSV and returns data rows, skipping the header. """
        records = []
        if os.path.isfile(self.spreadsheet_file_path):
            with open(self.spreadsheet_file_path, mode='r', newline='') as csv_file:
                csv_reader = csv.reader(csv_file)
                # Skip the header row
                next(csv_reader, None)  
                for row in csv_reader:
                    if row:
                        records.append(row)
        return records

    def get_stats(self):
        """ 
        The Stats Engine: Calculates 30, 60, and Lifetime MPG.
        Hard-coded logic for time-based performance tracking.
        """
        all_rows = self.read_all_records()
        
        # If there is no data, return zeros
        if not all_rows:
            return "0.00", "0.00", "0.00"

        # Define our time windows
        today = datetime.now()
        thirty_days_ago = today - timedelta(days=30)
        sixty_days_ago = today - timedelta(days=60)

        # Totals storage: [Miles, Gallons]
        total_30 = [0.0, 0.0]
        total_60 = [0.0, 0.0]
        total_life = [0.0, 0.0]

        for row in all_rows:
            try:
                # Extract date and numeric data from columns
                # row[0] = Date, row[4] = Miles, row[5] = Gallons
                row_date = datetime.strptime(row[0], "%Y-%m-%d")
                miles = float(row[4])
                gallons = float(row[5])

                # 1. Add to Lifetime totals
                total_life[0] = total_life[0] + miles
                total_life[1] = total_life[1] + gallons

                # 2. Check if within 30-day window
                if row_date >= thirty_days_ago:
                    total_30[0] = total_30[0] + miles
                    total_30[1] = total_30[1] + gallons

                # 3. Check if within 60-day window
                if row_date >= sixty_days_ago:
                    total_60[0] = total_60[0] + miles
                    total_60[1] = total_60[1] + gallons
                    
            except (ValueError, IndexError):
                # Skip rows with errors or empty columns
                continue

        # Final MPG calculations
        def calculate_mpg_safe(miles_val, gallons_val):
            if gallons_val > 0:
                result = miles_val / gallons_val
                return f"{result:.2f}"
            return "0.00"

        avg_30 = calculate_mpg_safe(total_30[0], total_30[1])
        avg_60 = calculate_mpg_safe(total_60[0], total_60[1])
        avg_life = calculate_mpg_safe(total_life[0], total_life[1])

        return avg_30, avg_60, avg_life

    def save_and_sort_data(self, new_row_data):
        """ Saves new load data and sorts the file. """
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)
            
        all_entries = self.read_all_records()
        all_entries.append(new_row_data)
        
        # Sort by Load ID then Date
        all_entries.sort(key=lambda x: (x[1], x[0]))
        
        with open(self.spreadsheet_file_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(self.header)
            csv_writer.writerows(all_entries)