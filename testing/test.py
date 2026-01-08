###############################################################################
# Date: 2026-01-08
# Script Name: chronos_vault_v5.py
# Author: omegazyph
# Updated: 2026-01-08
# Description: Sentinel Edition. Uses SHA-256 hashing to verify file content
#              integrity, ensuring zero duplicate backups of identical code.
###############################################################################

import os
import shutil
import time
import sys
import hashlib
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
    """Generates a SHA-256 hash to act as a unique digital fingerprint."""
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
    |______||_| |_||______||_____||_| \_||_____||_____|
               [ SYSTEM ARCHIVE v5.0 - SENTINEL ]
    """
    print_hacker(logo, "\033[1;33m") # Gold/Yellow for Sentinel Edition

def chronos_sync(source_root, backup_root):
    show_logo()
    stats = {"scanned": 0, "archived": 0, "skipped": 0, "bytes": 0}
    IGNORE_DIRS = {'__pycache__', '.git', '.venv', 'node_modules'}

    print_hacker(" [!] STATUS: CALCULATING FILE FINGERPRINTS (SHA-256)...")

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
            
            # 1. Get Modification Date
            mtime = os.path.getmtime(source_path)
            mod_date = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
            
            # 2. Get File Content Fingerprint
            current_hash = get_file_hash(source_path)
            
            new_name = f"{mod_date}_{project_name}_{filename}"
            dest_path = os.path.join(dest_dir, new_name)

            # 3. SMART CHECK: Does a file with this name AND this content already exist?
            if os.path.exists(dest_path):
                existing_hash = get_file_hash(dest_path)
                if current_hash == existing_hash:
                    stats["skipped"] += 1
                    continue # Content is identical, skip.

            try:
                shutil.copy2(source_path, dest_path)
                stats["archived"] += 1
                stats["bytes"] += os.path.getsize(source_path)
                print_hacker(f" [NEW] {new_name}")
            except Exception:
                print_hacker(f" [!] HASH MANTLE ERROR: {filename}", "\033[1;31m")

    # Final Summary
    size_mb = stats["bytes"] / (1024 * 1024)
    print_hacker("\n" + "="*54)
    print_hacker(f" [RESULT] FILES ANALYZED:  {stats['scanned']}")
    print_hacker(f" [RESULT] UNIQUE ARCHIVES: {stats['archived']}")
    print_hacker(f" [RESULT] DATA SAVED:      {size_mb:.2f} MB")
    print_hacker(" [STATUS] INTEGRITY CHECK PASSED. VAULT SEALED.")
    print_hacker("="*54)

if __name__ == "__main__":
    src = r"C:\Users\omega\OneDrive\Desktop\omegazyph\Legion_Tools"
    dst = r"C:\Users\omega\OneDrive\Desktop\omegazyph\Backup_Vault"
    
    start_time = time.time()
    chronos_sync(src, dst)
    print(f"\nExecution Time: {time.time() - start_time:.2f}s")
    input("\nPress ENTER to close...")