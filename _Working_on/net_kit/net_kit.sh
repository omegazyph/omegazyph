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
    source "${SCRIPT_DIRECTORY}/files/_Headers.sh"
else
    echo "Error: _Headers.sh not found in ${SCRIPT_DIRECTORY}. Please ensure it is present."
    exit 1
fi

# --- Operational Tool Functions ---

# Function to execute an IP sweep across a target subnet
run_ipsweep() {
    print_message "status" "Initializing IP sweep network discovery..."
    print_message "warning" "Scanning live hosts on the target subnet..."
    
    if [ -f "${SCRIPT_DIRECTORY}/files/ip sweep/ipsweep.sh" ]; then
        source "${SCRIPT_DIRECTORY}/files/ip sweep/ipsweep.sh"
    else
        print_message "error" "Error: ipsweep.sh not found in ${SCRIPT_DIRECTORY}. Please ensure it is present."
        exit 1
    fi
    
    print_message "success" "IP sweep completed successfully."
}

# Function to check local network interface status and connectivity
run_netcheck() {
    print_message "status" "Checking network interfaces and local connectivity..."
    print_message "warning" "Querying gateway and interface statistics..."
    
    # Place your actual netcheck logic here (e.g., ip a, route, or ping gateway)
    # Example placeholder delay simulating operation:
    sleep 2
    
    print_message "success" "Network status check completed."
}

# Function to execute a comprehensive network scan
run_scan_network() {
    print_message "status" "Initializing comprehensive network port scan..."
    print_message "warning" "Deep scans can take time; please remain patient..."
    
    # Place your actual scan_network logic here (e.g., nmap command routines)
    # Example placeholder delay simulating operation:
    sleep 3
    
    print_message "success" "Comprehensive network scan completed."
}

# --- Menu Display Function ---
show_menu() {
    echo -e ""
    echo -e "${BOLD}${CYAN}=== Select a Network Toolkit Operation ===${RESET}"
    echo -e "${GREEN}1)${RESET} IP Sweep (ipsweep)"
    echo -e "${GREEN}2)${RESET} Network Status Check (netcheck)"
    echo -e "${GREEN}3)${RESET} Comprehensive Network Scan (scan_network)"
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