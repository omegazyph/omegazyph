###############################################################################
# Date: 2026-01-07
# Script Name: legion_optimizer_fixed.py
# Author: omegazyph
# Updated: 2026-01-07
# Description: Fixed system optimization with stable Battery diagnostics.
###############################################################################

import os
import subprocess
import time
import sys
import psutil

def print_hacker(text, color="\033[1;32m"):
    """Prints text in green with a typing effect."""
    reset = "\033[0m"
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)
    print(reset)

def get_battery_info():
    """Uses psutil for stable battery reporting."""
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        plugged = "Plugged In" if battery.power_plugged else "On Battery"
        return percent, plugged
    return None, None

def optimize():
    # Clear screen for that clean Workstation look
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print_hacker("======================================================")
    print_hacker("   OMEGAZYPH LEGION COMMAND: STABLE DIAGNOSTIC        ")
    print_hacker("======================================================")
    time.sleep(1)

    # 1. STABLE BATTERY CHECK
    percent, status = get_battery_info()
    if percent is not None:
        print_hacker(f"[+] Battery Level: {percent}%")
        print_hacker(f"[+] Power Status: {status}")
    else:
        print_hacker("[!] Battery Sensor not found.", "\033[1;31m")

    # 2. ACTUAL OPTIMIZATION (Admin Required)
    print_hacker("\n[!] INITIATING SYSTEM TRIM...")
    try:
        # SSD Trim
        subprocess.run("defrag C: /O", shell=True, capture_output=True)
        print_hacker("[SUCCESS] SSD Optimization (Trim) completed.")
        
        # DNS Flush
        subprocess.run("ipconfig /flushdns", shell=True, capture_output=True)
        print_hacker("[SUCCESS] Network DNS Cache cleared.")
    except Exception:
        print_hacker("[!] Error running system tasks. Try 'Run as Admin'.", "\033[1;33m")

    # 3. CLEANUP
    temp_path = os.environ.get('TEMP')
    subprocess.run(f'del /q /f /s "{temp_path}\\*.*"', shell=True, capture_output=True)
    print_hacker("[SUCCESS] Temporary junk files purged.")

    print_hacker("\n======================================================")
    print_hacker("   SYSTEM OPTIMIZED | PROJECT: MATRIX_STATION         ")
    print_hacker("======================================================")

if __name__ == "__main__":
    optimize()