"""
Date: 2026-01-10
Script Name: spyware_scanner.py
Author: omegazyph
Updated: 2026-01-10
Description: This program scans the Windows Registry 'Run' keys for persistence 
             mechanisms often used by spyware and allows the user to remove them.
"""

import winreg # Used to interact with the Windows Registry
import os

def scan_registry_persistence():
    # The registry path where programs are set to run at startup for the current user
    registry_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    try:
        # Open the key for reading
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_READ)
        
        print(f"{'ID':<5} | {'Application Name':<25} | {'File Path'}")
        print("-" * 70)
        
        entries = []
        index = 0
        while True:
            try:
                # Loop through all values under this registry key
                name, value, _ = winreg.EnumValue(key, index)
                entries.append((name, value))
                print(f"{index:<5} | {name:<25} | {value}")
                index += 1
            except OSError:
                # OSError marks the end of the list
                break
        
        winreg.CloseKey(key)
        return entries
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def delete_persistence_entry(entry_name):
    # Re-open the key with 'Set Value' permissions to allow deletion
    registry_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, entry_name)
        winreg.CloseKey(key)
        print(f"\n[!] Successfully removed: {entry_name}")
    except Exception as e:
        print(f"[X] Failed to delete entry: {e}")

if __name__ == "__main__":
    print("--- omegazyph's Spyware Persistence Scanner ---\n")
    found_apps = scan_registry_persistence()
    
    if found_apps:
        user_input = input("\nEnter the ID to remove an entry, or 'q' to quit: ")
        if user_input.isdigit():
            idx = int(user_input)
            if 0 <= idx < len(found_apps):
                app_to_remove = found_apps[idx][0]
                confirm = input(f"Confirm deletion of '{app_to_remove}'? (y/n): ")
                if confirm.lower() == 'y':
                    delete_persistence_entry(app_to_remove)
    else:
        print("No startup entries found in this registry hive.")