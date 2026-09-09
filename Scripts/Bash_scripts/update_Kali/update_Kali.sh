#!/bin/bash
###########################################################################
# Date:         2024-01-21
# Script Name:  update.Kali.sh
# Author:       Wayne Stock
# updated:      2026-09-08
# description:  This script automates system maintenance tasks on Debian/Ubuntu-based systems.
#               It performs updates, upgrades installed software, updates specific tools,
#               and then cleans up the system.
##################################################################################################

# Exit immediately if any command fails (for unattend automation)
set -e

echo "==================================================="
echo "      Starting Kali Linux System Maintenance."
echo "==================================================="
# --- Update Section ---
# This section ensures your system's package lists and installed software are up-to-date.

# 1. Check for available updates for your package lists.
echo -e "Checking for updates..."
sudo apt-get update -y

# 2. Full Distribut Upgrade
echo -e "\nUpgrading all packages, including Bash..."
sudo apt-get dist-upgrade -y

# 3. Install and update the Exploit Database package.
echo -e "\nInstalling and updating Exploit Database..."
sudo apt-get install exploitdb -y

# 4. Update the Searchsploit database itself.
echo -e "\nUpdating Searchsploit database...."
sudo apt-get searchsploit -u

# 5. Update Nmap's Scripting Engine (NSE) scripts.
echo -e "\nUpdating nmap script database...."
sudo nmap --script-updatedb

# --- Cleaning Section ---
# This section helps free up disk space by removing unneeded packages and downloaded files.

# 6. Remove automatically installed packages that are no longer needed by any other package.
echo -e "\nRemoving any obsolete packages and their configuration files..."
sudo apt-get autoremove --purge -y

# Remove downloaded package archive files that are no longer needed.
echo -e "\nRemoving any downloaded files that are no longer needed..."
sudo apt-get autoclean -y

# Verify the currently installed Bash version.
echo -e "\nVerify Bash Version..."
bash --version

echo "==================================================="
echo "      Kali Linux System Maintenance Finished."
echo "==================================================="

# Check if a reboot is required by system updates
if [ -f /var/run/reboot-required ]; then
    echo -e "Kernel or core libraries were updated. A system reboot is required."
    read -p "WOuld you like to reboot the system now? (y/N): " REBOOT_CHOICE
    if [["$REBOOT_CHOICE" =~ ^[Yy]$ ]]; then
        echo -e "Initiating system reboot...."
        /usr/sbin/reboot
    else
        echo -e "Reboot deferred. Please remember to reboot later."
    fi
else
    echo -e "No system reboot required."
fi