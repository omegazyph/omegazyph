"""
Date: 2026-01-05
Script Name: spyware_scanner.py
Author: omegazyph
Updated: 2026-01-10
Description: Unified tool that backups the registry 'Run' keys and 
             scans for startup persistence using an external whitelist.
"""

import winreg # Used to read/write Windows Registry
import os
import subprocess
from datetime import datetime

# --- AUTOMATIC PATH DETECTION ---
# Find the 'scripts' folder where THIS file lives
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Find the 'SecurityScannerProject' root folder
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

def load_whitelist():
    """Reads whitelist.txt from the PROJECT root folder."""
    whitelist_path = os.path.join(PROJECT_ROOT, "whitelist.txt")
    
    if not os.path.exists(whitelist_path):
        print(f"[*] Creating new whitelist at: {whitelist_path}")
        with open(whitelist_path, "w") as f:
            f.write("# Add safe app names here (one per line)\n")
        return []
    
    with open(whitelist_path, "r") as f:
        # Returns a list of cleaned names, ignoring empty lines and comments
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def run_backup():
    """Mandatory safety backup using reg.exe."""
    targets = {
        "HKCU": r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run",
        "HKLM": r"HKLM\Software\Microsoft\Windows\CurrentVersion\Run"
    }
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(PROJECT_ROOT, "backups")
    
    if not os.path.exists(backup_dir): 
        os.makedirs(backup_dir)

    print("[*] Creating Safety Checkpoints...")
    for label, path in targets.items():
        backup_file = os.path.join(backup_dir, f"{label}_{timestamp}.reg")
        # No more path mangling since we use Python subprocess list arguments
        subprocess.run(['reg', 'export', path, backup_file, '/y'], capture_output=True)
    return True

def scan_keys(whitelist):
    """Scans the Registry and filters results using the loaded whitelist."""
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    found = []
    
    # Target both Current User and Local Machine
    hives = [
        (winreg.HKEY_CURRENT_USER, "HKCU"),
        (winreg.HKEY_LOCAL_MACHINE, "HKLM")
    ]

    for hive, label in hives:
        try:
            # KEY_READ to view, KEY_WOW64_64KEY to ensure we see 64-bit apps on your Legion
            key = winreg.OpenKey(hive, reg_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
            index = 0
            while True:
                try:
                    name, val, _ = winreg.EnumValue(key, index)
                    # Filter: Only add if it's NOT in our whitelist.txt
                    if name not in whitelist:
                        found.append({"loc": label, "name": name, "val": val})
                    index += 1
                except OSError:
                    break # End of registry entries
            winreg.CloseKey(key)
        except PermissionError:
            print(f"[!] Access Denied: Run as Admin to scan {label}")
        except Exception as e:
            print(f"[!] Error scanning {label}: {e}")

    return found

if __name__ == "__main__":
    print("--- omegazyph Security Scanner ---")
    print(f"Project Root: {PROJECT_ROOT}\n")
    
    # 1. Load the external whitelist
    safe_apps = load_whitelist()
    
    # 2. Perform the mandatory backup
    if run_backup():
        print("[SUCCESS] Registry backups saved to /backups folder.")
        
        # 3. Perform the filtered scan
        print("[*] Scanning for unknown startup items...")
        items = scan_keys(safe_apps)
        
        if items:
            print(f"\n{'ID':<4} | {'Source':<8} | {'Name':<25} | {'Path'}")
            print("-" * 85)
            for idx, item in enumerate(items):
                print(f"{idx:<4} | {item['loc']:<8} | {item['name']:<25} | {item['val']}")
        else:
            print("\n[V] Scan Complete: No unknown items detected.")
    else:
        print("[ABORT] Backup failed. Check your permissions.")