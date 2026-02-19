# Date: 2026-02-18
# Script Name: safe_user_cleaner.py
# Author: omegazyph
# Updated: 2026-02-18
# Description: A security-conscious cleaning script that operates 
#              within standard user permissions to protect against malware.

import os
import shutil
import psutil

def clean_user_space():
    print("--- Wayne's Safe User-Space Clean ---")
    
    # We only target folders Wayne's account naturally owns
    user_temp = os.environ.get('TEMP')
    
    if user_temp and os.path.exists(user_temp):
        print(f"Cleaning User Temp: {user_temp}")
        files_cleaned = 0
        for item in os.listdir(user_temp):
            item_path = os.path.join(user_temp, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                    files_cleaned += 1
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    files_cleaned += 1
            except Exception:
                # Skip files currently open in VSCode or browser
                continue
        print(f"Removed {files_cleaned} items from your user profile.")

def clean_python_garbage(start_dir):
    print(f"\n--- Purging Cache in Projects: {start_dir} ---")
    # This specifically hunts for those __pycache__ folders you wanted gone
    for root, dirs, files in os.walk(start_dir):
        if '__pycache__' in dirs:
            path = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(path)
                print(f"Cleaned: {path}")
            except Exception as e:
                print(f"Skipped {path}: {e}")

if __name__ == "__main__":
    # Part 1: Clean the local temp files your account created
    clean_user_space()
    
    # Part 2: Clean your coding project directories
    # This uses the current folder where the script is sitting
    project_path = os.getcwd()
    clean_python_garbage(project_path)
    
    print("\nMaintenance complete! System remains secure in Standard User mode.")