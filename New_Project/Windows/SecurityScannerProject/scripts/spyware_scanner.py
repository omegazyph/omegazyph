"""
Date: 2026-01-05
Script Name: spyware_scanner.py
Author: omegazyph
Updated: 2026-01-11
Description: Complete security tool to backup, scan, and manage Windows 
             startup registry keys. Features a whitelist and web-search 
             investigation tool.
"""

import winreg
import os
import subprocess
import ctypes
import webbrowser
from datetime import datetime

# --- AUTOMATIC PATH DETECTION ---
# This ensures files are always created in your Project folder
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
    """Reads whitelist.txt and returns a list of application names."""
    if not os.path.exists(WHITELIST_PATH):
        print(f"[*] Creating new whitelist at: {WHITELIST_PATH}")
        with open(WHITELIST_PATH, "w") as f:
            f.write("# Add safe app names here (one per line)\n")
        return []
    
    with open(WHITELIST_PATH, "r") as f:
        # Ignore empty lines and lines starting with '#'
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def add_to_whitelist(app_name):
    """Appends a new application name to the whitelist file."""
    with open(WHITELIST_PATH, "a") as f:
        f.write(f"{app_name}\n")
    print(f"[+] '{app_name}' has been added to your whitelist.")

def run_backup():
    """Uses reg.exe to export startup keys to the backups folder."""
    targets = {
        "HKCU": r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run",
        "HKLM": r"HKLM\Software\Microsoft\Windows\CurrentVersion\Run"
    }
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(PROJECT_ROOT, "backups")
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    print("[*] Creating safety backups...")
    for label, path in targets.items():
        backup_file = os.path.join(backup_dir, f"{label}_{timestamp}.reg")
        # Run Windows native export command
        subprocess.run(['reg', 'export', path, backup_file, '/y'], capture_output=True)
    return True

def scan_keys(whitelist):
    """Scans HKCU and HKLM for startup entries not in the whitelist."""
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    found = []
    hives = [
        (winreg.HKEY_CURRENT_USER, "HKCU"),
        (winreg.HKEY_LOCAL_MACHINE, "HKLM")
    ]

    for hive_const, label in hives:
        try:
            # KEY_READ to view, KEY_WOW64_64KEY for 64-bit Windows 11 compatibility
            key = winreg.OpenKey(hive_const, reg_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
            index = 0
            while True:
                try:
                    name, val, _ = winreg.EnumValue(key, index)
                    if name not in whitelist:
                        found.append({"hive": hive_const, "loc": label, "name": name, "val": val})
                    index += 1
                except OSError:
                    break # End of entries
            winreg.CloseKey(key)
        except Exception as e:
            if "Access is denied" in str(e):
                # Silently fail for HKLM if not admin, but keep scanning HKCU
                pass
            else:
                print(f"[!] Error scanning {label}: {e}")
    return found

def delete_entry(hive, name):
    """Removes a specific value from the Windows registry."""
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        # Requires KEY_SET_VALUE permissions
        key = winreg.OpenKey(hive, reg_path, 0, winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY)
        winreg.DeleteValue(key, name)
        winreg.CloseKey(key)
        print(f"\n[SUCCESS] '{name}' removed from startup.")
        return True
    except PermissionError:
        print("\n[!] ERROR: Permission Denied. You must run this script as Administrator.")
    except Exception as e:
        print(f"\n[!] ERROR: Could not delete entry: {e}")
    return False

def investigate_item(app_name):
    """Opens a Google search to research the safety of an item."""
    query = f"https://www.google.com/search?q={app_name}+windows+startup+safe+or+spyware"
    print(f"[*] Investigating: {app_name}")
    webbrowser.open(query)

if __name__ == "__main__":
    admin_status = "Admin" if is_admin() else "Standard User"
    print(f"--- omegazyph Security Scanner ({admin_status}) ---")
    print(f"Working Directory: {PROJECT_ROOT}\n")
    
    # 1. Start with a backup
    if run_backup():
        while True:
            # 2. Refresh whitelist and scan
            safe_apps = load_whitelist()
            items = scan_keys(safe_apps)
            
            print(f"\n[ Scan Results - {len(items)} Unknown Items ]")
            if items:
                print(f"{'ID':<4} | {'Source':<8} | {'Name':<25}")
                print("-" * 45)
                for idx, item in enumerate(items):
                    print(f"{idx:<4} | {item['loc']:<8} | {item['name']:<25}")
                
                print("\nOptions:")
                print(" [ID]  Add to Whitelist (e.g., 0)")
                print(" [sID] Search/Investigate (e.g., s0)")
                print(" [dID] Delete from Registry (e.g., d0)")
                print(" [r]   Rescan | [q] Quit")
            else:
                print("No unknown items found. Your startup is clean!")
                print("\nOptions: [r] Rescan | [q] Quit")

            cmd = input("\nSelection: ").strip().lower()
            
            if cmd == 'q':
                break
            elif cmd == 'r':
                continue
            elif cmd.isdigit():
                idx = int(cmd)
                if 0 <= idx < len(items):
                    add_to_whitelist(items[idx]['name'])
            elif cmd.startswith('s') and cmd[1:].isdigit():
                idx = int(cmd[1:])
                if 0 <= idx < len(items):
                    investigate_item(items[idx]['name'])
            elif cmd.startswith('d') and cmd[1:].isdigit():
                idx = int(cmd[1:])
                if 0 <= idx < len(items):
                    target = items[idx]
                    confirm = input(f"CONFIRM: Delete '{target['name']}'? (y/n): ")
                    if confirm.lower() == 'y':
                        delete_entry(target['hive'], target['name'])
            else:
                print("[!] Invalid input. Use numbers, sID, dID, r, or q.")
    else:
        print("[ABORT] Could not create a backup. Script stopped for safety.")