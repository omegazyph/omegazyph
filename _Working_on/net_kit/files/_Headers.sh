#!/usr/bin/env bash
##################################################################################################
# Date:         2026-09-13
# Script Name:  _Headers.sh
# Author:       Omegazyph
# Updated:      2026-09-16
# Description:  Core library providing ANSI colors, unified messaging, 
#               and dynamically centered ASCII banners.
# ==================================================================================================

# --- ANSI Color Codes ---
BLUE='\033[1;34m'
BOLD='\033[1m'
CYAN='\033[1;36m'
GREEN='\033[1;32m'
PURPLE='\033[1;35m'
RED='\033[1;31m'
RESET='\033[0m'
YELLOW='\033[1;33m'

# --- UI Functions ---

# Prints a dynamically centered starting ASCII banner
print_ascii_banner() {
    local banner_title="${1:-Default Title Starting}"
    local total_width=80
    local title_length=${#banner_title}
    local padding=$(( (total_width - title_length) / 2 ))
    
    # Generate the exact amount of leading spaces for centering
    local spaces=""
    for ((i = 0; i < padding; i++)); do
        spaces+=" "
    done

    echo -e "${PURPLE}================================================================================${RESET}"
    echo -e "${BOLD}${BLUE}${spaces}${banner_title}${RESET}"
    echo -e "${PURPLE}================================================================================${RESET}"
}

# Prints a dynamically centered closing ASCII banner
print_ascii_ending() {
    local ending_title="${1:-Default Title Ending}"
    local total_width=80
    local title_length=${#ending_title}
    local padding=$(( (total_width - title_length) / 2 ))
    
    # Generate the exact amount of leading spaces for centering
    local spaces=""
    for ((i = 0; i < padding; i++)); do
        spaces+=" "
    done

    echo -e "${PURPLE}================================================================================${RESET}"
    echo -e "${BOLD}${BLUE}${spaces}${ending_title}${RESET}"
    echo -e "${PURPLE}================================================================================${RESET}"
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

# --- Main Process ---
main() {
    # Display the startup banner
    print_ascii_banner "Put your Title here"

    # Execute operational status messages
    print_message "status" "Scanning for active devices on your network"
    print_message "info" "this is a info line"
    print_message "warning" "Please wait, this may take a few seconds"
    print_message "success" "Scan complete!"
    print_message "error" "No devices detected."

    # Displaying the ending banner
    print_ascii_ending "Put your ending title here"
}

