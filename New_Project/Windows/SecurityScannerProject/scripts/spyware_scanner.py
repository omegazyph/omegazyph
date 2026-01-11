"""
Date: 2026-01-05
Script Name: spyware_scanner.py
Author: omegazyph
Updated: 2026-01-11
Description: A professional-grade CLI tool for managing Windows startup.
             Features color-coded output, formatted tables, and intuitive commands.
"""

import winreg
import os
import subprocess
import ctypes
import webbrowser
from datetime import datetime

# --- COLORS & UI ---
# ANSI escape codes for a better terminal experience
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

def is_admin():
    try: 
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception: 
        return False

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
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
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

def delete_entry(hive, name):
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        key = winreg.OpenKey(hive, reg_path, 0, winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY)
        winreg.DeleteValue(key, name)
        winreg.CloseKey(key)
        print(f"{GREEN}[SUCCESS] Entry removed.{RESET}")
        return True
    except Exception as e:
        print(f"{RED}[ERROR] {e}{RESET}")
    return False

def print_header(admin):
    os.system('cls' if os.name == 'nt' else 'clear')
    status = f"{GREEN}Administrator{RESET}" if admin else f"{YELLOW}Standard User{RESET}"
    print(f"{BOLD}{BLUE}==============================================={RESET}")
    print(f"{BOLD}{BLUE}   OMEGAZYPH REGISTRY SCANNER - v2.0{RESET}")
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
                print(f" {GREEN}[ID]{RESET}  Whitelist   {BLUE}[sID]{RESET} Search   {RED}[dID]{RESET} Delete   {BOLD}[r]{RESET} Rescan   {BOLD}[q]{RESET} Quit")
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
                    print(f"{CYAN}[*] Opening browser...{RESET}")
                    webbrowser.open(f"https://www.google.com/search?q={items[idx]['name']}+startup")
            elif cmd.startswith('d') and cmd[1:].isdigit():
                idx = int(cmd[1:])
                if idx < len(items):
                    confirm = input(f"{RED}⚠ Confirm Delete '{items[idx]['name']}'? (y/n): {RESET}")
                    if confirm.lower() == 'y':
                        delete_entry(items[idx]['hive'], items[idx]['name'])