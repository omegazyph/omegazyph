#!/bin/env bash

# ===========================================================================
# Date:         2026-02-27
# Script Name:  update_Ubuntu.sh
# Author:       omegazyph
# Updated:      2026-11-23
# Description:  Professional system update script for Ubuntu-server.
#               Handles repository updates, upgrades, system cleanup,
#               and error handling.
# ===========================================================================

# Exit immediately if a command exits with a non-zero status
set -e

# region --- ANSI Color Codes ---
# Define ANSI escape sequences for terminal colors and text formatting
BLUE='\033[1;34m'
BOLD='\033[1m'
CYAN='\033[1;36m' #defualt color
GREEN='\033[1;32m'
MAGENTA='\033[38;2;255;0;144m'
PURPLE='\033[1;35m'
RED='\033[1;31m'
RESET='\033[0m'
YELLOW='\033[1;33m'
# endregion

# region --- User Interface Functions ---

# Print text in a specified ANSI color and reset formatting afterward
print_color() {
    local message_text="$1"
    local text_color="${2:-$CYAN}"

    # Output the colored string followed by a terminal attribute reset
    printf "%b%s%b\n" "${text_color}" "${message_text}" "${RESET}"
}

# Print a dynamically centered ASCII banner with top and bottom borders
print_ascii_banner() {
    local banner_title="${1:-Default Title Starting}"
    local total_width=65
    local title_length=${#banner_title}
    local padding=0

    # Calculate leading spaces only when the title is shorter than total_width
    if (( total_width > title_length )); then
        padding=$(( (total_width - title_length) / 2 ))
    fi

    # Build the exact number of leading spaces needed to center the title
    local leading_spaces=""
    local index=0
    for (( index = 0; index < padding; index++ )); do
        leading_spaces+=" "
    done

    # Build the horizontal border line matching total_width
    local border_line=""
    for (( index = 0; index < total_width; index++ )); do
        border_line+="="
    done

    # Print the top purple border, centered bold blue title, and bottom border
    print_color "${border_line}" "${PURPLE}"
    print_color "${leading_spaces}${banner_title}" "${BOLD}${BLUE}"
    print_color "${border_line}" "${PURPLE}"
}

# Print formatted messages with distinct prefixes and colors by message type
print_message() {
    local message_type="$1"
    local message_text="$2"

    # Match the requested message type to its corresponding prefix and color
    case "${message_type}" in
        "error")
            print_color "[X] ${message_text}" "${BOLD}${RED}"
            ;;
        "info")
            # Use [*] in BLUE for general informational notes
            print_color "[*] ${message_text}" "${BOLD}${BLUE}"
            ;;
        "status")
            # Use [~] in 24-bit MAGENTA for active status and progress updates
            print_color "[~] ${message_text}" "${BOLD}${MAGENTA}"
            ;;
        "success")
            print_color "[+] ${message_text}" "${BOLD}${GREEN}"
            ;;
        "warning")
            print_color "[!] ${message_text}" "${BOLD}${YELLOW}"
            ;;
        *)
            # Print plain uncolored text when no known category is provided
            printf "%s\n" "${message_text}"
            ;;
    esac
}
# endregion

# region --- Main Process ---
main() {
    # Clear terminal screen for a clean starting canvas
    clear

    print_ascii_banner "Ubuntu MAINTENANCE"


    # 1. Update package lists
    print_message "status" "─── [ Step 1/4 ] Updating Package Repositories ─────────────────"
    sudo apt update
    echo ""

    # 2. Upgrade packages
    print_message "status" "─── [ Step 2/4 ] Performing System Upgrade ─────────────────────"
    sudo apt upgrade -y
    echo ""

    # 3. Distribution upgrade (for kernel updates and dependencies)
    print_message "status" "─── [ Step 3/4 ] Running Distribution Upgrade ──────────────────"
    sudo apt dist-upgrade -y
    echo ""

    # 4. Cleanup old packages, cache, and check disk space
    print_message "status" "─── [ Step 4/4 ] Cleaning System & Checking Disk Space ─────────"
    sudo apt autoremove -y
    sudo apt autoclean
    sudo apt clean
    echo ""

    print_message "info" "Current Disk Usage:"
    df -h /
    echo ""

    # read the used percentage on / without the % sign (for example 85)
    local used_percent
    used_percent=$(df -P / | awk 'NR==2 {gsub(/%/, "", $5); print $5}')

    # Warn at 80% used or higher, and show an error at 90% used or higher
    if (( used_percent >= 90 )); then
        print_message "error" "Critically low disk space on / (${used_percent}% used)."
    elif (( used_percent >= 80 )); then
        print_message "warning" "Low disk space on / (${used_percent}% used)."
    fi

    # Print completion banner
    print_ascii_banner "MAINTENANCE COMPLETE"
    echo ""

    # Check if a reboot is required by checking the system flag
    if [ -f /var/run/reboot-required ]; then
    print_ascii_banner "*** SYSTEM RESTART REQUIRED ***"
    echo ""
    read -r -p "Would you like to reboot now? (y/n): " choice
    
    # Convert input to lowercase to support 'Y' or 'y'
    choice=$(echo "$choice" | tr '[:upper:]' '[:lower:]')
    
    if [ "$choice" == "y" ] || [ "$choice" == "yes" ]; then
        print_message "status" "Rebooting system in 5 seconds..."
        sleep 5
        sudo reboot
    else
        print_message "warning" "Reboot skipped. Please remember to restart the server manually."
    fi
else
    print_message "success" "No system reboot is necessary."
fi
echo ""
}
#endregion

# Execute main only when this script is run dirctly rather then sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then 
    main "$@"
fi