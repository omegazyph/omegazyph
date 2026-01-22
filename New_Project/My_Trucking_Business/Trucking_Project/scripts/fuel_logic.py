# ---------------------------------------------------------------------------
# Date: 2026-01-11
# Script Name: fuel_logic.py
# Author: omegazyph
# Updated: 2026-01-22
# Description: Logic and Data Handling for the Fuel Tracker.
#              This module handles file I/O, double-sorting (Load then Date),
#              and the safety feature to delete the last recorded entry.
# ---------------------------------------------------------------------------

import os
import csv

class FuelDataManager:
    def __init__(self, spreadsheet_file_path):
        """
        Initializes the manager with the path to the CSV file.
        The path is provided by the main script to ensure folder consistency.
        """
        self.spreadsheet_file_path = spreadsheet_file_path
        self.data_directory = os.path.dirname(spreadsheet_file_path)
        
        # Standardized header for the CSV to ensure column consistency
        self.header = [
            "Date", "Load ID", "Starting Miles", "Ending Miles", 
            "Total Trip Miles", "Gallons Used", "Fuel Cost USD", 
            "MPG", "Fuel CPM"
        ]

    def read_all_records(self):
        """
        Helper method to read the current state of the CSV file.
        Returns the header and a list of all data rows.
        """
        records = []
        if os.path.isfile(self.spreadsheet_file_path):
            with open(self.spreadsheet_file_path, mode='r', newline='') as csv_file:
                csv_reader = csv.reader(csv_file)
                # Capture the header row first
                current_header = next(csv_reader, self.header)
                # Capture all remaining data rows
                for row in csv_reader:
                    if row:
                        records.append(row)
            return current_header, records
        return self.header, []

    def save_and_sort_data(self, new_row_data):
        """
        Accepts a new list of data, combines it with existing records,
        sorts the entire list, and overwrites the file.
        """
        # Ensure the 'data' folder exists before trying to write
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)

        # Get existing data from the file
        header, all_entries = self.read_all_records()

        # Add the new record provided by the user interface
        all_entries.append(new_row_data)

        # DOUBLE SORT LOGIC:
        # x[1] is the Load ID (Primary Sort)
        # x[0] is the Date (Secondary Sort - used if Load IDs are identical)
        all_entries.sort(key=lambda x: (x[1], x[0]))

        # Overwrite the file with the fresh, sorted list
        self._write_to_disk(header, all_entries)

    def delete_last_saved_entry(self):
        """
        Safety Feature: Removes the very last row of the file and saves.
        This is useful if the user realizes they made a typo.
        """
        header, all_entries = self.read_all_records()
        
        if not all_entries:
            return False, "The spreadsheet is already empty."

        # Remove the last item in the list
        all_entries.pop()

        # Save the shortened list back to the CSV
        self._write_to_disk(header, all_entries)
        return True, "Last entry has been successfully removed."

    def _write_to_disk(self, header, data_rows):
        """
        Internal method (shorthand names avoided: 'private-style' method)
        to handle the actual file writing process.
        """
        with open(self.spreadsheet_file_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)
            csv_writer.writerows(data_rows)