###############################################################################
# Date: 2026-01-08
# Script Name: chronos_vault.py
# Author: omegazyph
# Updated: 2026-01-08
# Description: Sentinel Edition. Detects if a file already has a date prefix.
#              If found, it skips adding a new date to prevent "Double Dating."
###############################################################################

import os
import shutil
import time
import sys
import hashlib
import re
from datetime import datetime

def print_hacker(text, color="\033[1;32m"):
    reset = "\033[0m"
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.001)
    print(reset)

def get_file_hash(file_path):
    hasher = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return None

def show_logo():
    logo = r"""
     _______  _   _  ______  _____  _   _  _____  _____ 
    |  ____|| | | ||  ____||  _  || \ | ||  _  ||  ___|
    | |     | |_| || | __  | | | ||  \| || | | || |___ 
    | |     |  _  || |__ | | | | || \ \ || | | ||___  |
    | |____ | | | || |___| | |_| || |\  || |_| | ___| |
    |______||_| |_||______| \_____/|_| \_||_____/|_____|
               [ SYSTEM ARCHIVE v5.3 - SMART ]
    """
    print_hacker(logo, "\033[1;33m")

def chronos_sync(source_root, backup_root):
    show_logo()
    stats = {"scanned": 0, "archived": 0, "skipped": 0, "bytes": 0}
    IGNORE_DIRS = {'__pycache__', '.git', '.venv', 'node_modules'}

    # Regex pattern to match YYYY-MM-DD_ at the start of a string
    date_pattern = r"^\d{4}-\d{2}-\d{2}_"

    print_hacker(" [!] STATUS: SCANNING FOR EXISTING DATE SIGNATURES...")

    for root, dirs, files in os.walk(source_root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        rel_path = os.path.relpath(root, source_root)
        dest_dir = os.path.join(backup_root, rel_path)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        project_name = os.path.basename(root) if root != source_root else "Main"

        for filename in files:
            stats["scanned"] += 1
            source_path = os.path.join(root, filename)
            
            # --- SMART DATE CHECK ---
            if re.match(date_pattern, filename):
                # File already has a date! Keep it as is.
                new_name = f"{project_name}_{filename}"
            else:
                # No date found. Add the Modification Date.
                mtime = os.path.getmtime(source_path)
                mod_date = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
                new_name = f"{mod_date}_{project_name}_{filename}"
            
            dest_path = os.path.join(dest_dir, new_name)
            current_hash = get_file_hash(source_path)

            if os.path.exists(dest_path):
                if current_hash == get_file_hash(dest_path):
                    stats["skipped"] += 1
                    continue 

            try:
                shutil.copy2(source_path, dest_path)
                stats["archived"] += 1
                stats["bytes"] += os.path.getsize(source_path)
                print_hacker(f" [OK] {new_name}")
            except Exception:
                print_hacker(f" [!] ERROR: {filename}", "\033[1;31m")

    #size_mb = stats["bytes"] / (1024 * 1024)
    print_hacker("\n" + "="*54)
    print_hacker(" [RESULT] VAULT SYNC COMPLETE")
    print_hacker(f" [RESULT] FILES PROCESSED: {stats['scanned']}")
    print_hacker(f" [RESULT] NEW ARCHIVES:    {stats['archived']}")
    print_hacker("="*54)

if __name__ == "__main__":
    src = r"C:\Users\omega\OneDrive\Desktop\omegazyph\Legion_Tools"
    dst = r"C:\Users\omega\OneDrive\Desktop\omegazyph\Backup_Vault"
    chronos_sync(src, dst)
    input("\nPress ENTER to close...")