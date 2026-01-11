"""
Date: 2026-01-05
Script Name: spyware_scanner.py
Author: omegazyph
Updated: 2026-01-11
Description: Unified tool that backups and scans registry startup keys.
             Includes a whitelist filter and interactive deletion capabilities.
"""

import winreg
import os
import subprocess
import ctypes
from datetime import datetime

# --- PATH DETECTION ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
WHITELIST_PATH = os.path.join(PROJECT_ROOT, "whitelist.txt")

def is_admin():
    """Checks if the script is running with Administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def load_whitelist():
    """Reads whitelist.txt and returns a list of names."""
    if not os.path.exists(WHITELIST_PATH):
        with open(WHITELIST_PATH, "w") as f:
            f.write("# Add safe app names here (one per line)\n")
        return []
    with open(WHITELIST_PATH, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def add_to_whitelist(app_name):
    """Appends a name to the whitelist.txt."""
    with open(WHITELIST_PATH, "a") as f:
        f.write(f"{app_name}\n")
    print(f"[+] '{app_name}' added to whitelist.")

def run_backup():
    """Creates a .reg backup of the startup keys."""
    targets = {"HKCU": r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run",
               "HKLM": r"HKLM\Software\Microsoft\Windows\CurrentVersion\Run"}
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(PROJECT_ROOT, "backups")
    if not os.path.exists(backup_dir): 
        os.makedirs(backup_dir)

    for label, path in targets.items():
        backup_file = os.path.join(backup_dir, f"{label}_{timestamp}.reg")
        subprocess.run(['reg', 'export', path, backup_file, '/y'], capture_output=True)
    return True

def scan_keys(whitelist):
    """Scans registry hives and filters out whitelisted items."""
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    found = []
    hives = [(winreg.HKEY_CURRENT_USER, "HKCU"), (winreg.HKEY_LOCAL_MACHINE, "HKLM")]

    for hive_const, label in hives:
        try:
            # We open with KEY_READ to simply view the list first
            key = winreg.OpenKey(hive_const, reg_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
            index = 0
            while True:
                try:
                    name, val, _ = winreg.EnumValue(key, index)
                    if name not in whitelist:
                        found.append({"hive": hive_const, "loc": label, "name": name, "val": val})
                    index += 1
                except OSError:
                    break
            winreg.CloseKey(key)
        except Exception as e:
            if "Access is denied" in str(e):
                print(f"[!] {label} Scan: Run as Admin to see system keys.")
    return found

def delete_entry(hive, name):
    """Safely removes a specific value from a registry key."""
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        # KEY_SET_VALUE is the specific permission needed to delete/edit
        key = winreg.OpenKey(hive, reg_path, 0, winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY)
        winreg.DeleteValue(key, name)
        winreg.CloseKey(key)
        print(f"\n[SUCCESS] '{name}' deleted from registry.")
        return True
    except PermissionError:
        print("\n[!] ERROR: Permission Denied. Please run VSCode/Terminal as Administrator.")
    except Exception as e:
        print(f"\n[!] ERROR: {e}")
    return False

if __name__ == "__main__":
    print(f"--- omegazyph Security Scanner (Admin: {is_admin()}) ---")
    
    if run_backup():
        while True:
            safe_apps = load_whitelist()
            items = scan_keys(safe_apps)
            
            print(f"\n[ Scan Results - {len(items)} Unknown Items ]")
            if items:
                print(f"{'ID':<4} | {'Source':<8} | {'Name':<25}")
                print("-" * 45)
                for idx, item in enumerate(items):
                    print(f"{idx:<4} | {item['loc']:<8} | {item['name']:<25}")
                
                print("\nOptions: [ID] Whitelist | [d+ID] Delete (ex: d0) | [r] Rescan | [q] Quit")
            else:
                print("Your startup is clean!")
                print("\nOptions: [r] Rescan | [q] Quit")

            cmd = input("\nSelection: ").strip().lower()
            
            if cmd == 'q': 
                break
            elif cmd == 'r': 
                continue
            elif cmd.isdigit(): # Whitelist if user enters just a number
                idx = int(cmd)
                if idx < len(items): 
                    add_to_whitelist(items[idx]['name'])
            elif cmd.startswith('d') and cmd[1:].isdigit(): # Delete if user enters 'd0'
                idx = int(cmd[1:])
                if idx < len(items):
                    target = items[idx]
                    confirm = input(f"CONFIRM: Delete '{target['name']}' from {target['loc']}? (y/n): ")
                    if confirm == 'y':
                        delete_entry(target['hive'], target['name'])
            else:
                print("[!] Invalid input.")