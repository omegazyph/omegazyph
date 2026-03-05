"""
Date: 2026-01-05
Script Name: smart_backup.py
Author: omegazyph
Updated: 2026-01-06

Description: 
An incremental backup script optimized for VS Code. 
Copies new/modified files from 'my_files' to 'backup_folder'.
"""

import os
import shutil

def run_backup():
    # In VS Code, the 'Current Working Directory' can sometimes be the root 
    # folder of your workspace. This line ensures we find the script's actual folder.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    source_folder = os.path.join(script_dir, "my_files")
    backup_folder = os.path.join(script_dir, "backup_folder")

    # Safety check: Ensure the source exists
    if not os.path.exists(source_folder):
        print(f"[-] Error: Folder '{source_folder}' not found.")
        print("    Tip: Right-click 'my_files' in VS Code and select 'Copy Path' to verify.")
        return

    # Create backup folder if missing
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
        print(f"[+] Created new backup folder at: {backup_folder}")

    files = os.listdir(source_folder)
    copied_count = 0
    skipped_count = 0

    # Logic: Only copy if file is new or modified
    for file_name in files:
        source_path = os.path.join(source_folder, file_name)
        dest_path = os.path.join(backup_folder, file_name)

        if os.path.isfile(source_path):
            if os.path.exists(dest_path):
                # Compare modified times
                if os.path.getmtime(source_path) <= os.path.getmtime(dest_path):
                    skipped_count += 1
                    continue 
            
            shutil.copy2(source_path, dest_path)
            copied_count += 1
            print(f"[*] Updated: {file_name}")

    # Summary Output
    print("\n" + "="*30)
    print("      BACKUP COMPLETE")
    print("="*30)
    print(f"Files Updated: {copied_count}")
    print(f"Files Skipped: {skipped_count}")
    print("="*30)

if __name__ == "__main__":
    run_backup()