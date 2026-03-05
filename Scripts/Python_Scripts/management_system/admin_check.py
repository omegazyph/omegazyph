# Date: 2026-02-18
# Script Name: admin_check.py
# Author: omegazyph
# Updated: 2026-02-18
# Description: Checks if the current Python process has 
#              Administrator privileges on Wayne's Windows 11.

import ctypes
import os

def is_admin():
    try:
        # This checks for Admin status on Windows
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":
    print("--- Wayne's Permission Audit ---")
    if is_admin():
        print("RESULT: [ ADMIN ] You have full power. Temp cleaning will work.")
    else:
        print("RESULT: [ USER ] Limited power. C:\\Windows\\Temp will stay locked.")
        print("\nTo fix: Right-click VSCode and select 'Run as Administrator'.")