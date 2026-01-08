###############################################################################
# Date: 2026-01-07
# Script Name: legion_to_external_backup.py
# Author: omegazyph
# Updated: 2026-01-07
# Description: Syncs 'omegazyph' Desktop folder to LaCie (Z:).
#              Features hacker-style UI and incremental sync logic.
###############################################################################

import os
import shutil
import time
import sys

def print_hacker(text, color="\033[1;32m"):
    """Prints text with a techy typing effect in Matrix Green."""
    reset = "\033[0m"
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.008) # Fast typing for a pro feel
    print(reset)

def run_backup():
    # Clear screen for that clean workstation look
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print_hacker("======================================================")
    print_hacker("   OMEGAZYPH SECURE SYNC PROTOCOL: LACIE_Z_DRIVE      ")
    print_hacker("======================================================")
    time.sleep(0.5)

    # --- CONFIGURATION ---
    source_folder = r"C:\Users\omega\OneDrive\Desktop\omegazyph"
    backup_destination = r"Z:\Windows\Documents\Git hub projects\omegazyph_back_up"

    # 1. Drive Connection Check
    print_hacker("[!] PROBING HARDWARE: LACIE Z: ...")
    if not os.path.exists("Z:\\"):
        print_hacker("[-] ERROR: LaCie Drive (Z:) not found. Plug it in.", "\033[1;31m")
        return
    print_hacker("[SUCCESS] DRIVE Z: ONLINE.")

    # 2. Source Check
    if not os.path.exists(source_folder):
        print_hacker(f"[-] ERROR: Source folder '{source_folder}' missing.", "\033[1;31m")
        return

    # 3. Create destination if missing
    if not os.path.exists(backup_destination):
        print_hacker("[!] DESTINATION MISSING. CREATING DIRECTORY...")
        os.makedirs(backup_destination)

    print_hacker("\n[*] INITIATING SYNC: DESKTOP -> LACIE")
    print_hacker("------------------------------------------------------")

    updated = 0
    skipped = 0

    # 4. Sync Logic
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
                # Use a fast print for the files to look like a data stream
                print(f"\033[1;32m    [+] {name}\033[0m")
            else:
                skipped += 1

    # 5. Final Report
    print_hacker("\n" + "="*40)
    print_hacker("         BACKUP SUCCESSFUL")
    print_hacker("="*40)
    print_hacker(f"  Files Updated: {updated}")
    print_hacker(f"  Files Already Up-to-date: {skipped}")
    print_hacker("="*40)
    print_hacker("\n>>> SESSION SECURE. READY FOR NEW DATA.")

if __name__ == "__main__":
    run_backup()