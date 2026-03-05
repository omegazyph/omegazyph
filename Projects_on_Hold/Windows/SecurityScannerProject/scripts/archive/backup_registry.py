"""
Date: 2026-01-10
Script Name: backup_registry.py
Author: omegazyph
Updated: 2026-01-10
Description: A Python-based backup tool that exports the Windows 'Run' registry 
             key to a .reg file before any modifications are made.
"""

import subprocess
import os
from datetime import datetime

def backup_run_key():
    # Define the registry path (Raw string 'r' handles backslashes perfectly)
    reg_path = r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run"
    
    # Create a timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Define and create the backup directory
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"[*] Created directory: {backup_dir}")

    backup_file = os.path.join(backup_dir, f"backup_{timestamp}.reg")

    print(f"[*] Attempting to backup: {reg_path}")

    try:
        # Use subprocess to run the Windows reg export command
        # shell=True is used here to ensure the command is recognized by the Windows shell
        result = subprocess.run(
            ['reg', 'export', reg_path, backup_file, '/y'],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"[SUCCESS] Backup saved to: {backup_file}")
            return True
        else:
            print(f"[ERROR] Registry export failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    backup_run_key()