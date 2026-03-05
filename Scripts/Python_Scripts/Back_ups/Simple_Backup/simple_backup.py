"""
Date: 2026-01-05
Script Name: simple_backup.py
Author: omegazyph
Updated: 2026-01-06

Description: 
This program automatically finds its own location and copies files 
from a 'my_files' folder to a 'backup_folder'.
"""

import os
import shutil

def run_backup():
    # Get the absolute path of the directory where THIS script is saved
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Join that path with your folder names to create a "Full Path"
    source_folder = os.path.join(script_dir, "my_files")
    backup_folder = os.path.join(script_dir, "backup_folder")

    # Check if the source folder actually exists at that path
    if not os.path.exists(source_folder):
        print(f"Error: Could not find '{source_folder}'")
        print("Please make sure the folder is named correctly.")
        return

    # Create the backup folder if it doesn't exist
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
        print(f"Created backup directory at: {backup_folder}")

    # List files and start the loop
    files = os.listdir(source_folder)
    
    if not files:
        print("The source folder is empty.")
        return

    for file_name in files:
        source_path = os.path.join(source_folder, file_name)
        destination_path = os.path.join(backup_folder, file_name)

        if os.path.isfile(source_path):
            shutil.copy2(source_path, destination_path)
            print(f"Backed up: {file_name}")

def main():
    print("--- Starting Backup Process ---")
    run_backup()
    print("--- Backup Complete ---")

if __name__ == "__main__":
    main()