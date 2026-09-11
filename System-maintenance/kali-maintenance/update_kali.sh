#!/usr/bin/env bash
###########################################################################
# Date:         2024-01-21
# Script Name:  update_kali.sh
# Author:       Omegazyph
# updated:      2026-09-10
# Description:  This script automates system maintenance tasks on Debian/Ubuntu-based systems.
#               It performs updates, upgrades installed software, updates specific tools,
#               and then cleans up the system.
##################################################################################################


# ANSI Color Codes
BOLD='\033[1m'
CYAN='\033[1;36m'
GREEN='\033[1;32m'
BLUE='\033[1;34m'
PURPLE='\033[1;35m'
YELLOW='\033[1;33m'
RED='\033[1;31m'
RESET='\033[0m'

# Output Functions
print_ascii_banner() {
    echo -e "${CYAN}================================================================================${RESET}"
    echo -e "${BOLD}${CYAN}                    KALI LINUX AUTOMATED SYSTEM MAINTENANCE                     ${RESET}"
    echo -e "${CYAN}================================================================================${RESET}"
}

print_status() {
    echo -e "\n${BOLD}${CYAN}[*] $1...${RESET}"
}

print_success() {
    echo -e "${BOLD}${GREEN}[+] $1${RESET}"
}

print_warning() {
    echo -e "${BOLD}${YELLOW}[!] $1${RESET}"
}

print_error() {
    echo -e "${BOLD}${RED}[X] $1${RESET}"
}

# Main Process
print_ascii_banner


# Ensure script is executed with root privileges
if [ "$EUID" -ne 0 ]; then
    print_error "Error: This script must be run as root."
    exit 1
fi

# --- Network & DNS Integrity Check ---
# fix DNS resolution issues caused by Network Manager overwriting /etc/resolv.conf
print_status "Verifying DNS resolution..."
if ! ping -c 1 kali.org > /dev/null 2>&1; then
    print_error "DNS resolution failed. Applying static DNS configuration..."

    # Remove immutable attribute if already set, write DNS server, and relock
    chattr -i /etc/resolv.conf 2>/dev/null || true
    echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > /etc/resolv.conf
    chattr +i /etc/resolv.conf

    print_success "Static DNS servers (1.1.1.1 / 8.8.8.8) configured and locked."
else
    print_success "DNS resolution functioning properly."
fi


# --- Update Section ---
# This section ensures your system's package lists and installed software are up-to-date.


# Check for available updates for your package lists.
print_status "Checking for updates..."
if apt-get update; then 
    print_success "Updates was completed successfully"
else
    print_warning "Failed to update"
fi


# Full Distribution Upgrade
print_status "Upgrading installed packages"
if apt-get dist-upgrade -y; then
    print_success "Package upgrade Completed"
else
    print_warning "Package upgrade encountered issues"
fi

# Verify Kernel Headers and Image Meta-Packages
print_status "Updating held kernel headers and image meta-packages"
if apt-get install linux-headers-amd64 linux-image-amd64 -y --allow-change-held-packages; then
    print_success "Kernel meta-packages verified and updated"
else
    print_warning "Kernel meta-package update skipped or failed"
fi


# Install and update the Exploit Database package.
print_status "Installing and updating Exploit Database..."
if apt-get install exploitdb -y; then 
    print_success "Exploit Database update complete"
else
    print_warning "Exploit Database encountered an issue"
fi

# Update the Searchsploit database itself.
print_status "Updating Searchsploit database...."
timeout 60 searchsploit -u > /dev/null 2>&1
SEARCHSPLOIT_EXIT_CODE=$?
if [ "$SEARCHSPLOIT_EXIT_CODE" -eq 0 ] || [ "$SEARCHSPLOIT_EXIT_CODE" -eq 1 ]; then 
    print_success "Searchsploit database verified and up to date"
else
    print_warning "Searchsploit update encountered an issue"
fi

# Update Nmap's Scripting Engine (NSE) scripts.
print_status "Updating nmap script database...."
if nmap --script-updatedb; then 
    print_success "Nmap script database Updated successfully"
else
    print_warning "Failed to update Nmap script database"
fi

# --- Cleaning Section ---
# This section helps free up disk space by removing unneeded packages and downloaded files.

# Clean up orphaned packages and package cache
print_status "Cleaning up cached installer files and unneeded dependencies..."
if apt-get autoremove --purge -y && apt-get clean; then
    print_success "System cleanup complete successfully"
else
    print_warning "System cleanup encountered an issue"
fi

# Verify the currently installed Bash version.
print_status "Verify installed Bash Version"
if bash --version | head -n 1; then
    print_success "Bash version verified successfully"
else
    print_warning "Failed to retrieve Bash version"
fi


echo -e "${CYAN}===================================================${RESET}"
echo -e "${BOLD}${CYAN}          Kali Linux System Maintenance Finished.${RESET}"
echo -e "${CYAN}===================================================${RESET}"

# Check if a reboot is required by system updates
if [ -f /var/run/reboot-required ]; then
    print_warning "Kernel or core libraries were updated. A system reboot is required."
    read -p "Would you like to reboot the system now? (y/N): " REBOOT_CHOICE
    if [[ "$REBOOT_CHOICE" =~ ^[Yy]$ ]]; then
        print_status "Initiating system reboot...."
        /usr/sbin/reboot
    else
        print_warning "Reboot deferred. Please remember to reboot later."
    fi
else
    print_success "No system reboot required."
fi