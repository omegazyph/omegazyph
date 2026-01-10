"""
Date: 2026-01-05
Script Name: spyware_scanner.py
Author: omegazyph
Updated: 2026-01-10
Description: Unified tool that backups the registry 'Run' keys and 
             then scans for startup persistence.
"""

import winreg
import os
import subprocess
from datetime import datetime

def run_backup():
    """Uses Windows reg.exe to create a safety checkpoint."""
    # We target both User and Machine hives for full security
    targets = {
        "HKCU": r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run",
        "HKLM": r"HKLM\Software\Microsoft\Windows\CurrentVersion\Run"
    }
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = "backups"
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    print("[*] Initializing Safety Backups...")
    
    all_success = True
    for label, path in targets.items():
        backup_file = os.path.join(backup_dir, f"{label}_{timestamp}.reg")
        # subprocess.run is the Pythonic way to call 'reg export'
        result = subprocess.run(['reg', 'export', path, backup_file, '/y'], 
                                capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"[SUCCESS] {label} backup created: {os.path.basename(backup_file)}")
        else:
            print(f"[!] Warning: {label} backup failed. (You may need Admin rights for HKLM)")
            if label == "HKCU": all_success = False # HKCU failure is a dealbreaker
            
    return all_success

def scan_keys():
    """Reads the registry to see what starts with Windows."""
    path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    found = []
    
    # Scan Current User
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_READ)
        i = 0
        while True:
            try:
                name, val, _ = winreg.EnumValue(key, i)
                found.append({"loc": "HKCU", "name": name, "val": val})
                i += 1
            except OSError: break
        winreg.CloseKey(key)
    except Exception as e:
        print(f"[ERROR] Could not scan HKCU: {e}")

    return found

if __name__ == "__main__":
    print("=== omegazyph Security Scanner (Windows 11) ===\n")
    
    # The backup happens AUTOMATICALLY here
    if run_backup():
        print("\n[*] Starting Registry Scan...")
        items = scan_keys()
        
        if items:
            print(f"\n{'ID':<4} | {'Source':<8} | {'Name':<25} | {'Path'}")
            print("-" * 85)
            for idx, item in enumerate(items):
                print(f"{idx:<4} | {item['loc']:<8} | {item['name']:<25} | {item['val']}")
        else:
            print("[*] No entries found.")
    else:
        print("[ABORT] Backup failed. Please check folder permissions.")