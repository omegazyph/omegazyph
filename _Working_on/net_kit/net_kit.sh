#!/usr/bin/env bash
# ===========================================================================================
# Date:         2026-09-13
# Script Name:  net_kit.sh
# Author:       Omegazyph
# Updated:      2026-09-16
# Description:  Modular network utility toolkit that sources _Headers.sh for UI 
#               components and provides a menu for IP sweep, netcheck, and scans.
# ===========================================================================================

# --- Anchor and Source Shared Headers ---
# This ensures the script finds _Headers.sh in the exact same directory,
# no matter where you execute the toolkit from in your terminal.
SCRIPT_DIRECTORY="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "${SCRIPT_DIRECTORY}/files/_Headers.sh" ]; then
    # shellcheck disable=SC1091
    source "${SCRIPT_DIRECTORY}/files/_Headers.sh"
else
    echo "Error: _Headers.sh not found in ${SCRIPT_DIRECTORY}. Please ensure it is present."
    exit 1
fi

# --- Operational Tool Functions ---

# Function to execute an IP sweep across a target subnet
run_ipsweep() {

    
    if [ -f "${SCRIPT_DIRECTORY}/files/ipsweep/ipsweep.sh" ]; then
        # shellcheck disable=SC1091
        source "${SCRIPT_DIRECTORY}/files/ipsweep/ipsweep.sh"
    else
        print_message "error" "Error: ipsweep.sh not found in ${SCRIPT_DIRECTORY}. Please ensure it is present."
        exit 1
    fi
    
    print_message "success" "IP sweep completed successfully."
}

# Function to check local network interface status and connectivity
run_netcheck() {
    if [ -f "${SCRIPT_DIRECTORY}/files/NetCheck.sh" ]; then
        # shellcheck disable=SC1091
        source "${SCRIPT_DIRECTORY}/files/Netcheck.sh"
    else
        print_message "error" "Error: ipsweep.sh not found in ${SCRIPT_DIRECTORY}. Please ensure it is present."
        exit 1
    fi    
    print_message "success" "Network status check completed."
}

# Function to execute a comprehensive network scan
run_scan_network() {
   if [ -f "${SCRIPT_DIRECTORY}/files/scan_network_kali.sh" ]; then
        # shellcheck disable=SC1091
        source "${SCRIPT_DIRECTORY}/files/scan_network_kali.sh"
    else
        print_message "error" "Error: ipsweep.sh not found in ${SCRIPT_DIRECTORY}. Please ensure it is present."
        exit 1
    fi 
    print_message "success" "Comprehensive network scan completed."
}

# --- Menu Display Function ---
show_menu() {
    echo -e ""
    echo -e "${BOLD}${CYAN}=== Select a Network Toolkit Operation ===${RESET}"
    echo -e "${GREEN}1)${RESET} IP Sweep (Kali/windows)"
    echo -e "${GREEN}2)${RESET} Network Status Check (Kali/windows)"
    echo -e "${GREEN}3)${RESET} Comprehensive Network Scan (need root permissions Kali only for now)"
    echo -e "${RED}4)${RESET} Exit Toolkit"
    echo -e ""
}

# --- Main Execution Controller ---
main() {
    local user_selection

    # Display the primary startup banner utilizing the sourced header function
    print_ascii_banner "Network Toolkit Operation"

    # Continuous loop to keep the menu active until the user decides to exit
    while true; do
        show_menu
        
        # Prompt the user for their menu choice on the same line
        echo -ne "${BOLD}${YELLOW}[?] Enter your choice [1-4]: ${RESET}"
        read -r user_selection

        case "$user_selection" in
            1)
                echo -e ""
                run_ipsweep
                ;;
            2)
                echo -e ""
                run_netcheck
                ;;
            3)
                echo -e ""
                run_scan_network
                ;;
            4)
                print_message "info" "Exiting network utility toolkit. Goodbye!"
                break
                ;;
            *)
                print_message "error" "Invalid selection. Please choose a valid option between 1 and 4."
                ;;
        esac
    done

    # Display closing banner utilizing the sourced header function
    print_ascii_ending "Thank you for using Network Toolkit"
}

# --- Script Execution Entry Point ---
main

# --- End of Script ---