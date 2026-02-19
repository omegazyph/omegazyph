# Date: 2026-02-18
# Script Name: legion_performance_kit.py
# Author: omegazyph
# Updated: 2026-02-18
# Description: Enhanced maintenance tool for Wayne's Legion. 
#              Handles PermissionErrors gracefully when cleaning temp folders.

import os
import shutil
import psutil
import gc

def clean_system():
    print("--- Phase 1: Cleaning Windows Temp ---")
    temp_folders = [os.environ.get('TEMP'), r'C:\Windows\Temp']
    
    for folder in temp_folders:
        if folder and os.path.exists(folder):
            print(f"Checking: {folder}")
            try:
                # This is where the PermissionError usually happens
                files = os.listdir(folder)
                for file in files:
                    try:
                        full_path = os.path.join(folder, file)
                        if os.path.isfile(full_path):
                            os.remove(full_path)
                        elif os.path.isdir(full_path):
                            shutil.rmtree(full_path)
                    except Exception:
                        continue # Skip specific files that are in use
            except PermissionError:
                print(f"Access Denied for {folder}. (Run as Admin to clean this).")
            except Exception as e:
                print(f"Could not process {folder}: {e}")
    print("Temp file processing finished.")

def purge_cache(start_path):
    print("\n--- Phase 2: Purging Python Cache ---")
    count = 0
    for root, dirs, files in os.walk(start_path):
        if '__pycache__' in dirs:
            cache_dir = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(cache_dir)
                print(f"Removed: {cache_dir}")
                count += 1
            except Exception:
                continue
    print(f"Purged {count} cache folders.")

def optimize_ram():
    print("\n--- Phase 3: Memory Status ---")
    mem = psutil.virtual_memory()
    print(f"Total RAM: {mem.total / (1024**3):.1f} GB")
    print(f"Current Usage: {mem.percent}%")
    
    gc.collect() # Python internal cleanup
    print("Memory optimization triggered.")

if __name__ == "__main__":
    clean_system()
    # Using the path from your error message
    work_dir = r"C:\Users\omega\Desktop\omegazyph\Scripts"
    purge_cache(work_dir)
    optimize_ram()