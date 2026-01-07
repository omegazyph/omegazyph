"""
Date: 2026-01-07
Script Name: legion_to_external_backup.py
Author: omegazyph
Updated: 2026-01-07

Description: 
Syncs the 'omegazyph' folder from the Desktop to the LaCie (Z:) drive.
Optimized for a Windows 11 Home Lenovo Legion setup.
"""

import os
import shutil

def run_backup():
    # --- CONFIGURATION ---
    # Finds the Desktop automatically
    desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
    source_folder = os.path.join(desktop_path, "omegazyph") 
    
    # Your specific deep folder path on the LaCie drive
    backup_destination = r"Z:\Windows\Documents\Git hub projects\omegazyph_back_up"

    # 1. Drive Connection Check
    if not os.path.exists("Z:\\"):
        print("[-] ERROR: LaCie Drive (Z:) not found. Please plug it in.")
        return

    # 2. Source Check
    if not os.path.exists(source_folder):
        print(f"[-] ERROR: Source folder '{source_folder}' not found.")
        return

    # 3. Create destination if missing
    if not os.path.exists(backup_destination):
        os.makedirs(backup_destination)

    print("[*] Syncing: Desktop/omegazyph --> Z: (LaCie)")

    updated = 0
    skipped = 0

    for root, dirs, files in os.walk(source_folder):
        # Skip .git folder to keep backup slim
        if '.git' in dirs:
            dirs.remove('.git')

        rel_path = os.path.relpath(root, source_folder)
        dest_dir = os.path.join(backup_destination, rel_path)

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        for name in files:
            s_file = os.path.join(root, name)
            d_file = os.path.join(dest_dir, name)

            # Incremental copy: only if changed or new
            if not os.path.exists(d_file) or os.path.getmtime(s_file) > os.path.getmtime(d_file):
                shutil.copy2(s_file, d_file)
                updated += 1
                print(f"    [+] {name}")
            else:
                skipped += 1

    print("\n" + "="*40)
    print("         BACKUP SUCCESSFUL")
    print("="*40)
    print(f"  Files Updated: {updated}")
    print(f"  Files Already Up-to-date: {skipped}")
    print("="*40)

if __name__ == "__main__":
    run_backup()