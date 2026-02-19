"""
Date: 2026-01-07
Script Name: legion_to_external_backup.py
Author: omegazyph
Updated: 2026-02-10
Description: Synchronizes multiple folders (Desktop and a new folder) to 
              the LaCie (Z:) drive. Features a loop-based sync engine 
              and hacker-style UI.
"""

import os
import shutil
import time
import sys

def print_hacker(text, color="\033[1;32m"):
    """Prints text with a techy typing effect."""
    reset = "\033[0m"
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.008)
    print(reset)

def sync_folders(source, destination):
    """
    Handles the actual incremental sync logic for a single pair of folders.
    Returns a tuple of (updated_count, skipped_count).
    """
    updated = 0
    skipped = 0

    if not os.path.exists(source):
        print_hacker(f"[-] ERROR: Source '{source}' missing. Skipping...", "\033[1;31m")
        return 0, 0

    if not os.path.exists(destination):
        os.makedirs(destination)

    for root, directories, files in os.walk(source):
        if '.git' in directories:
            directories.remove('.git')

        relative_path = os.path.relpath(root, source)
        dest_dir = os.path.join(destination, relative_path)

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        for filename in files:
            source_file = os.path.join(root, filename)
            destination_file = os.path.join(dest_dir, filename)

            if not os.path.exists(destination_file) or os.path.getmtime(source_file) > os.path.getmtime(destination_file):
                try:
                    shutil.copy2(source_file, destination_file)
                    updated += 1
                    print(f"\033[1;32m    [+] {filename}\033[0m")
                except Exception as error:
                    print(f"\033[1;31m    [!] Error copying {filename}: {error}\033[0m")
            else:
                skipped += 1
    return updated, skipped

def run_backup_protocol():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print_hacker("======================================================")
    print_hacker("   OMEGAZYPH MULTI-SYNC PROTOCOL: LACIE_Z_DRIVE       ")
    print_hacker("======================================================")

    # Check for drive connection
    if not os.path.exists("Z:\\"):
        print_hacker("[-] ERROR: LaCie Drive (Z:) not found.", "\033[1;31m")
        return

    # --- CONFIGURATION: ADD MORE FOLDERS HERE ---
    # Dictionary format: r"Source Path": r"Destination Path"
    backup_tasks = {
        r"C:\Users\omega\Desktop\omegazyph": r"Z:\Windows\Documents\Git hub projects\omegazyph_back_up",
        r"C:\Users\omega\Desktop\Freelance-Portfolio-Project": r"Z:\Windows\Documents\Git hub projects\Freelance-Portfolio-Project_Back_up"
    }

    total_updated = 0
    total_skipped = 0

    for source, destination in backup_tasks.items():
        print_hacker(f"\n[*] STARTING SYNC: {os.path.basename(source)} -> Z:")
        u, s = sync_folders(source, destination)
        total_updated += u
        total_skipped += s

    # Final Report
    print_hacker("\n" + "="*40)
    print_hacker("          ALL BACKUPS SUCCESSFUL")
    print_hacker("="*40)
    print_hacker(f"  Total Files Updated: {total_updated}")
    print_hacker(f"  Total Files Skipped: {total_skipped}")
    print_hacker("="*40)

if __name__ == "__main__":
    try:
        run_backup_protocol()
    except KeyboardInterrupt:
        print("\n\033[1;31m[!] Protocol Terminated.\033[0m")
        sys.exit()