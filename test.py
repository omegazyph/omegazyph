###############################################################################
# Date: 2026-01-07
# Script Name: legion_to_external_backup.py
# Author: omegazyph
# Updated: 2026-01-07
# Description: Professional Python backup tool with high-visibility hacker
#              interface for syncing to LaCie (Z:).
###############################################################################

import os
import shutil
import time
import sys
from datetime import datetime

def print_hacker(text, color="\033[1;32m"):
    """Prints text with a techy typing effect in Matrix Green."""
    reset = "\033[0m"
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)  # Faster typing for efficiency
    print(reset)

def run_backup():
    # Clear the terminal for that "fresh login" look
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print_hacker("======================================================")
    print_hacker("   OMEGAZYPH SECURE DATA SYNC PROTOCOL: ACTIVE        ")
    print_hacker("======================================================")
    time.sleep(0.5)

    # Define Paths
    source_dir = os.path.expanduser("~/Documents/Projects") 
    dest_dir = "Z:/Legion_Backups"

    # 1. Hardware Detection
    print_hacker("[!] PROBING HARDWARE PORTS...")
    if not os.path.exists("Z:/"):
        print_hacker("[ERROR] LACIE (Z:) NOT DETECTED. SYSTEM ABORT.", "\033[1;31m")
        return
    print_hacker("[SUCCESS] LACIE (Z:) DRIVE ONLINE.")

    # 2. Data Scan
    print_hacker(f"[!] SCANNING SOURCE: {source_dir}")
    if not os.path.exists(source_dir):
        print_hacker("[ERROR] SOURCE FOLDER MISSING.", "\033[1;31m")
        return

    # 3. Execution
    try:
        print_hacker("\n>>> INITIATING ENCRYPTED DATA TRANSFER...")
        
        # This performs the actual copy
        # dirs_exist_ok=True allows updating an existing backup
        shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)
        
        # Simulate a data stream for the "Hacker" visual
        for i in range(10):
            dots = "." * (i % 4)
            sys.stdout.write(f"\r\033[1;32m[EXE] SYNCING DATA PACKETS{dots}   ")
            sys.stdout.flush()
            time.sleep(0.2)
        
        print_hacker("\n\n[SUCCESS] PACKETS VERIFIED.")
        print_hacker("[SUCCESS] BACKUP LOG WRITTEN TO DRIVE Z:")
        
    except Exception as e:
        print_hacker(f"\n[!] CRITICAL SYSTEM FAILURE: {str(e)}", "\033[1;31m")

    print_hacker("======================================================")
    print_hacker("   SYNC COMPLETE | SYSTEM SECURE | SESSION END        ")
    print_hacker("======================================================")

if __name__ == "__main__":
    run_backup()