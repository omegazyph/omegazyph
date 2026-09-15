#!/usr/bin/env bash

# ==============================================================================
# Date:        2026-01-04
# Script name: NetCheck.sh
# Author:      omegazyph
# Updated:     2026-09-14
# DESCRIPTION: A security utility to scan the local network and identify 
#              connected devices.
# ==============================================================================

# --- ANSI Color Codes ---
BLUE='\033[1;34m'
BOLD='\033[1m'
CYAN='\033[1;36m'
GREEN='\033[1;32m'
PURPLE='\033[1;35m'
RED='\033[1;31m'
RESET='\033[0m'
YELLOW='\033[1;33m'

# --- Output files ---
script_directory="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
output_file="$script_directory/report.txt"

# --- FUNCTIONS ---
print_ascii_banner() {
    echo -e "${PURPLE}====================================================${RESET}"
    echo -e "${BOLD}${BLUE}            NETCHECK SECURITY SCANNER${RESET}"
    echo -e "${PURPLE}====================================================${RESET}"
}

# Unified message printing function
print_message() {
    local message_type="$1"
    local message_text="$2"

    case "$message_type" in
        "error")
            echo -e "${BOLD}${RED}[X] ${message_text}${RESET}"
            ;;
        "info")
            echo -e "${BOLD}${BLUE}[*] ${message_text}${RESET}"
            ;;
        "status")
            echo -e "${BOLD}${CYAN}[*] ${message_text}${RESET}"
            ;;
        "success")
            echo -e "${BOLD}${GREEN}[+] ${message_text}${RESET}"
            ;;
        "warning")
            echo -e "${BOLD}${YELLOW}[!] ${message_text}${RESET}"
            ;;
        *)
            echo -e "${message_text}"
            ;;
    esac
}


# --- MAIN PROCESS ---
# Display the main startup banner
print_ascii_banner

# Inform the user that the network table retriecal is beginning
print_message "status" "Scanning for active devices on your network\n"

# Retrieve Address Resolution Protocol table entries
devices=$(arp -a)

if [ -z "$devices" ]; then
    print_message "error" "ERROR: No devices detected or ARP table is empty."
    exit 1
fi

# --- THE REPORT ---

# Print header titles for the network report output
print_message "status" "INTERNET ADDRESS     PHYSICAL ADDRESS     TYPE\n"


# Filter and display valid IP address entries from the stored ARP table output
device_list=$(echo "$devices" | grep -E '([0-9]{1,3}\.){3}[0-9]{1,3}')
echo "$device_list"

# --- SUMMARY ---

# Calculate the total number of valid active IP entries found in the ARP Table
device_count=$(echo "$devices" | grep -Ec '^[[:space:]]+[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')

# Print the final summary block showing total active device discovered
echo -e "${PURPLE}================================================${RESET}"
echo -e "${BOLD}${BLUE}     SCAN COMPLETE: $device_count active entries found.${RESET}"
echo -e "${PURPLE}================================================${RESET}"

# --- SAVE REPORT TO TEXT FILE ---
{
    echo "===================================================="
    echo "            NETCHECK SECURITY SCANNER REPORT        "
    echo "            Date: $(date)                         "
    echo "===================================================="
    echo ""
    echo "INTERNET ADDRESS        PHYSICAL ADDRESS       TYPE"
    echo "$device_list"
    echo ""
    echo "===================================================="
    echo "      SCAN COMPLETE: $device_count active entries found."
    echo "===================================================="
} > "$output_file"

print_message "info" "Report successfully saved to $output_file"