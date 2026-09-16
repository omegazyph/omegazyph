#!/usr/bin/env bash

# ==============================================================================
# Date:        2025-05-20
# SCRIPT NAME: ipsweep.sh
# Author:      omegazyph
# Updated:     2026-09-13
# DESCRIPTION: Scans a /24 subnet for live hosts by pinging IPs from .1 to .254
# USAGE:       ./ipsweep.sh <subnet-prefix>  (e.g., ./ipsweep.sh 192.168.1)
# ==============================================================================

# Difine the target file to log the ip 
TARGET_FILE="ip_list.txt"

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
    echo -e "${PURPLE}=======================================================${RESET}"
    echo -e "${BOLD}${BLUE}                               KALI LINUX AUTOMATED IP SWEEP${RESET}"
    echo -e "${PURPLE}=======================================================${RESET}"
}

print_status() {
    local message="$1"
    echo -e "\n${BOLD}${CYAN}[*] ${message}${RESET}"
}
print_info() {
    local message="$1"
    echo -e "${BLUE}[*] INFO: ${message}${RESET}"
}

print_success() {
    local message="$1"
    echo -e "${BOLD}${GREEN}[+] ${message}${RESET}"
}

print_warning() {
    local message="$1"
    echo -e "${BOLD}${YELLOW}[!] ${message}${RESET}"
}

print_error() {
    local message="$1"
    echo -e "${BOLD}${RED}[X] ${message}${RESET}"
}

# Main Process
print_ascii_banner





# Check if a subnet argument was provided by the user
if [ -z "$1" ]; then
    print_info "No subnet prefix provided."
    print_warning "(Example: bash ipsweep.sh 192.168.1)"
    exit 1
fi


# Loop through numbers 1 to 254 to use as the last octet of the IP address
for ip in $(seq 1 254); do
    # Display inline status Bar
    printf "${CYAN}\r[*] Scanning: %s.%s (%d/254) ${RESET}\n" "$1" "$ip" "$ip"

    # Ping the target IP address once (-c 1), filter for successful replies, and extract the IP
     if ping -c 1 "$1.$ip" | grep "64 bytes"; then
        echo -e "$1.$ip" >> "$TARGET_FILE"
        print_success "Host is alive\n"
    else
        print_error "Nothing Here\n"

    fi

    # windows Testing only
    ##############################################################################################    
    # Ping the target IP address once (-c 1), filter for successful replies, and extract the IP
    # if ping -n 1 "$1.$ip" | grep "bytes=32" ; then
    #     echo -e "$1.$ip" >> "$TARGET_FILE"
    #     print_success "Host is alive\n"
    # else
    #     print_error "Nothing Here\n"

    # fi
    ###############################################################################################

done

# Wait for all background ping processes to complete before exiting the script
wait

echo -e "${PURPLE}=======================================================${RESET}"
echo -e "${BOLD}${BLUE}                               KALI LINUX AUTOMATED IP SWEEP COMPLETE${RESET}"
echo -e "${PURPLE}=======================================================${RESET}"