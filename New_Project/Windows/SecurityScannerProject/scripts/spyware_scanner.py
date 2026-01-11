"""
Date: 2026-01-05
Script Name: spyware_scanner.py
Author: omegazyph
Updated: 2026-01-11
Description: A professional-grade CLI tool for managing Windows startup.
             Now includes a persistent logging system to track all deletions.
"""

import winreg
import os
import subprocess
import ctypes
import webbrowser
from datetime import datetime

# --- COLORS & UI ---
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

# --- PATH DETECTION ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
WHITELIST_PATH = os.path.join(PROJECT_ROOT, "whitelist.txt")
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")

def is_admin():
    try: 
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception: 
        return False

def log_action(action, name, hive):
    """Saves a record of the action to the logs folder."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    log_file = os.path.join(LOG_DIR, "activity.log")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"[{timestamp}] ACTION: {action} | NAME: {name} | HIVE: {hive}\n"
    
    try:
        with open(log_file, "a") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"{RED}[!] Failed to write to log: {e}{RESET}")

def load_whitelist():
    if not os.path.exists(WHITELIST_PATH):
        with open(WHITELIST_PATH, "w") as f:
            f.write("# Add safe app names here (one per line)\n")
        return []
    with open(WHITELIST_PATH, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def add_to_whitelist(app_name):
    with open(WHITELIST_PATH, "a") as f:
        f.write(f"{app_name}\n")
    print(f"{GREEN}[+] '{app_name}' ignored successfully.{RESET}")

def run_backup():
    targets = {"HKCU": r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run",
               "HKLM": r"HKLM\Software\Microsoft\Windows\CurrentVersion\Run"}
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    backup_dir = os.path.join(PROJECT_ROOT, "backups")
    if not os.path.exists(backup_dir): 
        os.makedirs(backup_dir)

    print(f"{CYAN}[*] Creating registry checkpoints...{RESET}")
    for label, path in targets.items():
        backup_file = os.path.join(backup_dir, f"{label}_{timestamp}.reg")
        subprocess.run(['reg', 'export', path, backup_file, '/y'], capture_output=True)
    return True

def scan_keys(whitelist):
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    found = []
    hives = [(winreg.HKEY_CURRENT_USER, "HKCU"), (winreg.HKEY_LOCAL_MACHINE, "HKLM")]

    for hive_const, label in hives:
        try:
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
        except Exception: 
            pass
    return found

def delete_entry(hive, name, label):
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        key = winreg.OpenKey(hive, reg_path, 0, winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY)
        winreg.DeleteValue(key, name)
        winreg.CloseKey(key)
        
        # LOG THE DELETION
        log_action("DELETE", name, label)
        
        print(f"{GREEN}[SUCCESS] Entry removed and logged.{RESET}")
        return True
    except Exception as e:
        print(f"{RED}[ERROR] {e}{RESET}")
    return False

def print_header(admin):
    os.system('cls' if os.name == 'nt' else 'clear')
    status = f"{GREEN}Administrator{RESET}" if admin else f"{YELLOW}Standard User{RESET}"
    print(f"{BOLD}{BLUE}==============================================={RESET}")
    print(f"{BOLD}{BLUE}   OMEGAZYPH REGISTRY SCANNER - v3.0{RESET}")
    print(f"{BOLD}{BLUE}==============================================={RESET}")
    print(f" Status: {status} | {RED}Please Reboot your PC to take effect{RESET}\n")

if __name__ == "__main__":
    admin = is_admin()
    if run_backup():
        while True:
            safe_apps = load_whitelist()
            items = scan_keys(safe_apps)
            print_header(admin)
            
            if items:
                print(f"{BOLD}{'ID':<5} | {'Source':<8} | {'Application Name':<30}{RESET}")
                print("-" * 50)
                for idx, item in enumerate(items):
                    color = YELLOW if item['loc'] == "HKLM" else CYAN
                    print(f"{idx:<5} | {color}{item['loc']:<8}{RESET} | {item['name']:<30}")
                
                print(f"\n{BOLD}COMMANDS:{RESET}")
                print(f" {GREEN}[ID]{RESET} Whitelist  {BLUE}[sID]{RESET} Search  {RED}[dID]{RESET} Delete  {BOLD}[r]{RESET} Rescan  {BOLD}[q]{RESET} Quit")
            else:
                print(f"{GREEN}✔ Everything looks clean! No unknown items detected.{RESET}")
                print(f"\n{BOLD}COMMANDS:{RESET} [r] Rescan   [q] Quit")

            cmd = input(f"\n{BOLD}Select Action: {RESET}").strip().lower()
            
            if cmd == 'q': 
                break
            elif cmd == 'r': 
                continue
            elif cmd.isdigit() and int(cmd) < len(items):
                add_to_whitelist(items[int(cmd)]['name'])
            elif cmd.startswith('s') and cmd[1:].isdigit():
                idx = int(cmd[1:])
                if idx < len(items):
                    webbrowser.open(f"https://www.google.com/search?q={items[idx]['name']}+startup")
            elif cmd.startswith('d') and cmd[1:].isdigit():
                idx = int(cmd[1:])
                if idx < len(items):
                    confirm = input(f"{RED}⚠ Confirm Delete '{items[idx]['name']}'? (y/n): {RESET}")
                    if confirm.lower() == 'y':
                        delete_entry(items[idx]['hive'], items[idx]['name'], items[idx]['loc'])