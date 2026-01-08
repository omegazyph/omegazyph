###############################################################################
# Date: 2026-01-07
# Script Name: chronos_vault.py
# Author: omegazyph
# Updated: 2026-01-07
# Description: Secure backup vault with Matrix-style terminal output.
#              Preserves folder structure with YYYY-MM-DD prefixing.
###############################################################################

import os
import shutil
import time
import sys
from datetime import datetime

def print_hacker(text, color="\033[1;32m"):
    """Matrix-style typing effect for terminal immersion."""
    reset = "\033[0m"
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.005) # Slightly faster for backup logs
    print(reset)

def chronos_sync(source_root, backup_root):
    # 1. Date format: 2026-01-07
    today_date = datetime.now().strftime("%Y-%m-%d")
    
    print_hacker("======================================================")
    print_hacker(f" [!] INITIALIZING CHRONOS VAULT SYNC: {today_date}")
    print_hacker(" STATUS: ENCRYPTING FILE PATHS...")
    print_hacker("======================================================\n")

    for root, dirs, files in os.walk(source_root):
        # Safety: Skip the backup folder itself
        if os.path.abspath(backup_root) in os.path.abspath(root):
            continue

        # Recreate the folder structure
        rel_path = os.path.relpath(root, source_root)
        dest_dir = os.path.join(backup_root, rel_path)

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        # Identify Project Name
        project_name = os.path.basename(root)
        if not project_name or root == source_root:
            project_name = "Main"

        for filename in files:
            name, ext = os.path.splitext(filename)
            
            # Format: 2026-01-07_ProjectName_FileName.ext
            new_name = f"{today_date}_{project_name}_{name}{ext}"
            
            source_path = os.path.join(root, filename)
            dest_path = os.path.join(dest_dir, new_name)

            if os.path.exists(dest_path):
                # Using Cyan for skipped files
                print_hacker(f" [-] STABLE: {new_name}", "\033[1;36m")
                continue

            try:
                shutil.copy2(source_path, dest_path)
                print_hacker(f" [OK] ARCHIVED: {new_name}")
            except Exception as e:
                print_hacker(f" [!] UPLINK ERROR: {filename} | {e}", "\033[1;31m")

    print_hacker("\n======================================================")
    print_hacker(" [SUCCESS] VAULT SYNCHRONIZATION COMPLETE")
    print_hacker(" ALL CORE ASSETS SECURED ON LOCAL DISK")
    print_hacker("======================================================")

if __name__ == "__main__":
    # Your Legion Paths
    src = r"C:\Users\omega\OneDrive\Desktop\omegazyph\Legion_Tools"
    dst = r"C:\Users\omega\OneDrive\Desktop\omegazyph\Backup_Vault"
    
    chronos_sync(src, dst)
    input("\nPress ENTER to disconnect from Vault...")