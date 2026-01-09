###############################################################################
# Date: 2026-01-09
# Script Name: legion_sentinel.py
# Author: omegazyph
# Updated: 2026-01-09
# Description: Added Alarm Throttling to prevent constant beeping.
#              Uses a 30-second cooldown for battery alerts.
###############################################################################

import psutil
import time
import sys
import os
from datetime import datetime
import winsound

# Hacker Aesthetic Colors
G = "\033[1;32m"  
R = "\033[1;31m"  
C = "\033[1;36m"  
W = "\033[0m"     

# Global variable to store the last time the alarm sounded
last_beep_time = 0 

def boot_sequence():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = f"""
    {G}╔══════════════════════════════════════════════════════╗
    ║  LEGION SENTINEL v2.2 - SECURE INTERFACE             ║
    ║  OPERATOR: omegazyph                                 ║
    ╚══════════════════════════════════════════════════════╝{W}
    """
    print(banner)

def get_stats():
    global last_beep_time # Allows us to update the variable outside the function
    
    battery = psutil.sensors_battery()
    disk = psutil.disk_usage('C:')
    mem = psutil.virtual_memory()
    
    bat_color = G if battery.percent > 20 else R
    
    # --- ALARM LOGIC WITH COOLDOWN ---
    current_time = time.time()
    if battery.percent < 15 and not battery.power_plugged:
        # Check if 30 seconds have passed since the last beep
        if current_time - last_beep_time > 30:
            winsound.Beep(1000, 200) # Short, sharp chirp
            last_beep_time = current_time # Reset the cooldown timer
    
    return [
        (f"{C}[SYSTEM TIME]{W}", datetime.now().strftime("%H:%M:%S")),
        (f"{C}[CPU LOAD]{W}", f"{psutil.cpu_percent()}%"),
        (f"{C}[MEMORY]{W}", f"{mem.percent}%"),
        (f"{C}[STORAGE]{W}", f"{round(disk.free / (1024**3), 1)} GB Free"),
        (f"{bat_color}[BATTERY]{W}", f"{battery.percent}% ({'AC_PWR' if battery.power_plugged else 'DISCHG'})")
    ]

if __name__ == "__main__":
    boot_sequence()
    sys.stdout.write("\033[s") 

    try:
        while True:
            sys.stdout.write("\033[u")
            print(f"{G}[+] SENTINEL ACTIVE - COOLDOWN SYSTEM ENGAGED{W}\n")
            
            current_stats = get_stats()
            for label, value in current_stats:
                sys.stdout.write("\033[K") 
                print(f" {label.ljust(25)} >> {value}")
            
            # Pulse indicator
            sys.stdout.write(f"\n{G}█{W} STATUS: NOMINAL" if int(time.time()) % 2 == 0 else "\n  STATUS: NOMINAL")
            sys.stdout.flush()
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n\n{R}[!] SHUTTING DOWN SYSTEM MONITOR...{W}")