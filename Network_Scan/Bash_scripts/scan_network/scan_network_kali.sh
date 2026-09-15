#!/usr/bin/env bash

# ==============================================================================
# Date:        2025-05-23
# Script name: scan_network_kali.sh
# Author:      omegazyph
# Updated:     2026-09-15
# DESCRIPTION: Scans the local network using arp-scan and reports any MAC 
#              addresses that are not listed in the known_macs.txt allowlist.
# ==============================================================================

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
    echo -e "${PURPLE}====================================================${RESET}"
    echo -e "${BOLD}${BLUE}        KALI LINUX AUTOMATED NETWORK SCANER${RESET}"
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


# Main Process
print_ascii_banner


# Get the absolute directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set the network interface to scan (e.g., eth0 or wlan0)
INTERFACE="eth0"

# File containing known MAC addresses (one MAC address per line)
KNOWN_MACS_FILE="$SCRIPT_DIR/known_macs.txt"

# Verify that root privileges are active
if [ "$EUID" -ne 0 ]; then
    print_message "error" "Error: This script must be run with root privileges (sudo)."
    exit 1
fi

# Verify that the known MACs file exists
if [ ! -f "$KNOWN_MACS_FILE" ]; then
    print_message "error" "Error: Known MACs file not found at: $KNOWN_MACS_FILE"
    exit 1
fi

# Notify user the scan is starting on the specified interface
print_message "status" "Scanning on interface $INTERFACE..."

# Initialize an array to hold known MAC addresses in uppercase for consistent comparison
KNOWN_MAC_LIST=()
while read -r raw_mac_address; do
    # Skip empty lines or comment lines starting with a hash symbol
    if [[ -z "$raw_mac_address" || "$raw_mac_address" =~ ^# ]]; then
        continue
    fi

    # Convert the MAC address to uppercase for reliable matching
    MAC_CLEAN=$(echo "$raw_mac_address" | tr 'a-f' 'A-F')
    # Add the cleaned MAC to the known list
    KNOWN_MAC_LIST+=("$MAC_CLEAN")
done < "$KNOWN_MACS_FILE"

# Use arp-scan to scan the local network on the chosen interface
# Filter output lines that contain a valid MAC address pattern
arp-scan --interface="$INTERFACE" --localnet | grep -Ei "([0-9a-f]{2}:){5}[0-9a-f]{2}" | while read -r IP MAC VENDOR; do
    # Convert the scanned MAC to uppercase for comparison
    MAC_UPPER=$(echo "$MAC" | tr 'a-f' 'A-F')

    # Attempt reverse DNS lookup with a 1-second timeout to get hostname for the IP
    HOSTNAME=$(host -W 1 "$IP" 2>/dev/null | awk '/domain name pointer/ {print $5}' | sed 's/\.$//')

    # If no hostname found, set to a default label
    if [ -z "$HOSTNAME" ]; then
        HOSTNAME="(no DNS name)"
    fi

    # Flag to check if MAC is known
    IS_KNOWN=false

    # Check each known MAC against the scanned MAC
    for KNOWN_MAC in "${KNOWN_MAC_LIST[@]}"; do
        if [[ "$MAC_UPPER" == "$KNOWN_MAC" ]]; then
            IS_KNOWN=true
            break
        fi
    done

    # If MAC is not known, print details about the unknown device
    if [ "$IS_KNOWN" = false ]; then
        print_message "warning" "UNKNOWN: $IP  $MAC  $HOSTNAME  $VENDOR"
    fi
done

echo -e "${PURPLE}=====================================================${RESET}"
echo -e "${BOLD}${BLUE}              KALI LINUX AUTOMATED NETWORK SCANER COMPLETE${RESET}"
echo -e "${PURPLE}=====================================================${RESET}"
