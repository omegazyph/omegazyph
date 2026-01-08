###############################################################################
# Date: 2026-01-07
# Script Name: file_ghost_organizer.py
# Author: omegazyph
# Updated: 2026-01-07
# Description: Automatically sorts the Downloads folder into categorized 
#              subfolders to keep the Legion C: drive optimized.
###############################################################################

import os
import shutil
import time
import sys

def print_hacker(text, color="\033[1;32m"):
    reset = "\033[0m"
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)
    print(reset)

def organize_downloads():
    os.system('cls')
    print_hacker("======================================================")
    print_hacker("   OMEGAZYPH FILE GHOST: DOWNLOADS RECLAMATION        ")
    print_hacker("======================================================")

    # Path Configuration
    download_path = os.path.expanduser("~/Downloads")
    
    # Define categories and their extensions
    destinations = {
        "Scripts": [".py", ".sh", ".bat", ".ps1"],
        "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
        "Media": [".jpg", ".png", ".mp4", ".mp3"],
        "Installers": [".exe", ".msi"],
        "Archives": [".zip", ".rar", ".7z"]
    }

    print_hacker(f"[*] SCANNING: {download_path}")
    time.sleep(1)

    count = 0
    for filename in os.listdir(download_path):
        file_ext = os.path.splitext(filename)[1].lower()
        
        for category, extensions in destinations.items():
            if file_ext in extensions:
                dest_folder = os.path.join(download_path, category)
                
                # Create category folder if it doesn't exist
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                
                # Move the file
                try:
                    shutil.move(os.path.join(download_path, filename), 
                                os.path.join(dest_folder, filename))
                    print(f"\033[1;32m    [MOVING] {filename} -> {category}\033[0m")
                    count += 1
                except Exception:
                    print(f"\033[1;31m    [ERROR] Could not move {filename}\033[0m")

    print_hacker("------------------------------------------------------")
    print_hacker(f"[SUCCESS] {count} FILES CATEGORIZED AND RECLAIMED.")
    print_hacker("======================================================")

if __name__ == "__main__":
    organize_downloads()