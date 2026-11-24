#!/usr/bin/env bash

# =============================================================================
# Date:           2026-09-13
# Script Name:    bash_starter.sh
# Author:         Omegazyph
# Updated:        2026-11-23
# Description:    Core Bash starter library providing ANSI terminal colors,
#                 unified status messaging, and dynamically centered banners.
# File Structure: project_root/
#                     bash_starter.sh
# =============================================================================

# region --- ANSI Color Codes ---
# Define ANSI escape sequences for terminal colors and text formatting
BLUE='\033[1;34m'
BOLD='\033[1m'
CYAN='\033[1;36m'
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
    # Clear the terminal screen before displaying startup output
    clear

    # Display the opening banner
    print_ascii_banner "Put your Title here"

    # Demonstrate each supported status and notification category
    print_message "status" "Scanning for active devices on your network"
    print_message "info" "This is an informational line"
    print_message "warning" "Please wait, this may take a few seconds"
    print_message "success" "Scan complete!"
    print_message "error" "No devices detected."

    # Display the closing banner
    print_ascii_banner "Put your ending title here"
}
# endregion

# Execute main only when this script is run directly rather than sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi