#!/usr/bin/env python3
"""
==============================================================================
SCRIPT NAME:    system_update.py
DESCRIPTION:    Automated System Hardening & Maintenance Utility.
                Updates core packages, ExploitDB, Nmap scripts, and 
                cleans obsolete files to reduce the attack surface.
AUTHOR:         Wayne Stock
DATE:           Jan 4, 2026
VERSION:        1.1
==============================================================================
"""

import subprocess
#import sys

def run_command(description, command):
    """
    Helper function to execute shell commands with clean output and error handling.
    """
    print(f"\n[*] {description}...")
    try:
        # shell=True allows for piped commands; capture_output gathers text for processing
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"[SUCCESS] {description} completed.")
            if result.stdout:
                # Truncate output to show only the first few lines of the success result
                print(result.stdout.strip()[:300] + "...") 
        else:
            print(f"[ERROR] {description} failed with return code {result.returncode}")
            print(f"Details: {result.stderr.strip()}")
            
    except Exception as e:
        print(f"[CRITICAL] Unexpected error during {description}: {str(e)}")

def main():
    """
    Main execution sequence for system hardening.
    """
    print("====================================================")
    print("      LEVEL 7 SYSTEM HARDENING & UPDATE TOOL")
    print("====================================================\n")

    # 1. Update Package Lists
    # Ensures the system knows about the latest security patches
    run_command("Refreshing package repositories", "sudo apt-get update -y")

    # 2. Upgrade Packages
    # dist-upgrade handles changing dependencies in new versions of packages
    run_command("Upgrading system packages and Bash", "sudo apt-get dist-upgrade -y")

    # 3. Security Tools: Exploit Database
    # Installs or updates the local copy of the Exploit Database
    run_command("Installing/Updating ExploitDB", "sudo apt-get install exploitdb -y")

    # 4. Security Tools: Searchsploit
    # Updates the command-line search tool for ExploitDB
    run_command("Updating Searchsploit database", "sudo searchsploit -u")

    # 5. Security Tools: Nmap NSE
    # Updates the Nmap Scripting Engine database for vulnerability scanning
    run_command("Updating Nmap Scripting Database (NSE)", "sudo nmap --script-updatedb")

    # 6. System Sanitization: Autoremove
    # Removes packages that were installed as dependencies but are no longer needed
    run_command("Purging obsolete packages", "sudo apt-get autoremove --purge -y")

    # 7. System Sanitization: Autoclean
    # Clears out the local repository of retrieved package files (.deb)
    run_command("Cleaning package cache", "sudo apt-get autoclean -y")

    # 8. Version Verification
    # Final check to ensure Bash is updated to the latest available version
    run_command("Verifying Bash Version", "bash --version")

    print("\n" + "="*52)
    print("      SYSTEM MAINTENANCE AND HARDENING COMPLETE")
    print("="*52 + "\n")

if __name__ == "__main__":
    # Execute the maintenance suite
    main()