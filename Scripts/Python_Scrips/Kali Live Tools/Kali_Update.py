"""
Date: 2026-01-13
File Name: kali_updater.py
Author: omegazyph
Updated: 2026-01-13

Description: 
A Python-based update manager for Kali Linux Live Persistence.
Handles system locks, checks disk space, and ensures graphical 
dependencies (xinit) are maintained. Enhanced with live output 
streaming and execution timers.
"""

import subprocess
import os
import shutil
import sys
import time

# ANSI Color codes
class Color:

	G = '\033[1;92m' #Success
	R = '\033[1;91m' #Errors
	W = '\033[97m' #info
	Y = '\033[1;93m' #warnings


def header():
	print(f"{Color.G}#########################################################################################{Color.W}")
	print(f"{Color.G}#                             Kali Linux Updater V3.0                                   #{Color.W}")
	print(f"{Color.G}#                                  By Omegazyph                                         #{Color.W}")
	print(f"{Color.G}#                         Updates Kali live with Persistence                            #{Color.W}")
	print(f"{Color.G}#########################################################################################{Color.W}")

def run_command(command):
    """
    MODDED: Now uses Popen to stream terminal output live and 
    includes a timer to monitor performance.
    """
    print(f"{Color.G}\n[EXEC] Running: {command}{Color.W}")
    start_time = time.time()
    
    try:
        # Popen allows us to see the output (like progress bars) live
        process = subprocess.Popen(
            command, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True,
            bufsize=1
        )

        # Stream the output to the VSCode terminal
        for line in process.stdout:
            print(f"  > {line}", end="")
            sys.stdout.flush()

        process.wait()
        end_time = time.time()
        duration = end_time - start_time
        
        if process.returncode == 0:
            print(f"{Color.G}[OK] Completed in {duration:.2f} seconds.{Color.W}")
            return True
        else:
            print(f"{Color.R}[!] Command failed with exit code {process.returncode}{Color.W}")
            return False
            
    except Exception as e:
        print(f"{Color.R}[!] Python Error: {e}{Color.W}")
        return False

def check_environment():
    """Verify disk space and persistence health before updating."""
    print(f"{Color.G}--- Checking Environment ---{Color.W}")
    
    # Check for /persistence or root space
    total, used, free = shutil.disk_usage("/")
    free_gb = free // (2**30)
    
    if free_gb < 3:
        print(f"{Color.Y}[!] Low Disk Space: {free_gb}GB. Update might be risky.{Color.W}")
    else:
        print(f"{Color.G}[OK] Available Space: {free_gb}GB{Color.W}")

    # Clear locks if they exist from a previous crash
    lock_path = "/var/lib/dpkg/lock-frontend"
    if os.path.exists(lock_path):
        print(f"{Color.Y}[!] Found DPKG lock. Cleaning up...{Color.W}")
        # Finish the interrupted install if it exists
        run_command("sudo rm /var/lib/dpkg/lock-frontend")
        run_command("sudo dpkg --configure -a")

def perform_update():
    """Execute the core update logic with real-time feedback."""
    print(f"{Color.G}\n--- Starting Update Process ---{Color.W}")
    
    # 1. Update package lists
    print(f"{Color.G}[1/4] Updating Package Lists...{Color.W}")
    run_command("sudo apt update")
    
    # 2. Ensure xinit is present (Fixing the error from yesterday)
    print(f"{Color.G}[2/4] Verifying Graphical Dependencies (xinit)...{Color.W}")
    run_command("sudo apt install -y xinit xorg kali-desktop-xfce")
    
    # 3. Full Distribution Upgrade
    print(f"{Color.G}[3/4] Performing Distribution Upgrade...{Color.W}")
    run_command("sudo apt dist-upgrade -y")
    
    # 4. Clean up unnecessary files to save space on the 50GB USB
    print(f"{Color.G}[4/4] Cleaning up cache...{Color.W}")
    run_command("sudo apt autoremove -y && sudo apt autoclean")
    
    print(f"{Color.G}\nUpdate Cycle Complete!{Color.W}")

if __name__ == "__main__":

    header()	
    # Ensure script is run as root for apt commands
    if os.geteuid() != 0:
        print(f"{Color.Y}Please run this script with 'sudo'.{Color.W}")
    else:
        check_environment()
        perform_update()
