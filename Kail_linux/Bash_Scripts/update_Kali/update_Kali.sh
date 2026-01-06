#!/bin/bash
# Author: Wayne Stock
# Date: 2024-01-21
# update 2025-07-07

# This script automates system maintenance tasks on Debian/Ubuntu-based systems.
# It performs updates, upgrades installed software, updates specific tools,
# and then cleans up the system.
# This script is a direct translation of the provided Python script.

# --- Update Section ---
# This section ensures your system's package lists and installed software are up-to-date.

# Check for available updates for your package lists.
echo "Checking for updates..."
# 'sudo apt-get update -y' refreshes the list of packages from repositories.
# The '-y' flag automatically confirms prompts.
sudo apt-get update -y

# Upgrade all installed packages to their latest versions.
echo -e "\nUpgrading all packages, including Bash..."
# 'sudo apt-get dist-upgrade -y' performs a full system upgrade, handling dependencies.
# This updates core system components like the Bash shell.
sudo apt-get dist-upgrade -y

# Install and update the Exploit Database package.
echo -e "\nInstalling and updating Exploit Database..."
# 'sudo apt-get install exploitdb -y' installs the package that includes searchsploit.
sudo apt-get install exploitdb -y

# Update the Searchsploit database itself.
echo -e "\nUpdating Searchsploit database...."
# NOTE: The original Python script had "sudo apt-get searchsploit -u".
# The correct command to update the Searchsploit database is 'searchsploit -u'.
searchsploit -u

# Update Nmap's Scripting Engine (NSE) scripts.
echo -e "\nUpdating nmap script database...."
# 'sudo nmap --script-updatedb' fetches the latest versions of Nmap's scripts.
sudo nmap --script-updatedb

# --- Cleaning Section ---
# This section helps free up disk space by removing unneeded packages and downloaded files.

# Remove automatically installed packages that are no longer needed by any other package.
echo -e "\nRemoving any obsolete packages and their configuration files..."
# 'sudo apt-get autoremove --purge -y' removes unused dependencies and their config files.
sudo apt-get autoremove --purge -y

# Remove downloaded package archive files that are no longer needed.
echo -e "\nRemoving any downloaded files that are no longer needed..."
# 'sudo apt-get autoclean -y' cleans the local repository of old or broken package files.
sudo apt-get autoclean -y

# Verify the currently installed Bash version.
echo -e "\nVerify Bash Version..."
# 'bash --version' displays information about the Bash shell.
bash --version