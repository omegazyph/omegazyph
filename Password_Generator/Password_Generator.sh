#!/usr/bin/env bash

# ===========================================================================================
# Date:         2025-07-08
# Script Name:  Password_Generator.sh
# Author:       Omegazyph 
# Updated:      2026-09-15 
# Description:  This script generates a random password of a specified length
#               using the OpenSSL utility. It utilizes base64 encoding to ensure
#               a diverse set of characters (alphanumeric, symbols).
# ============================================================================================

# --- ANSI Color Codes ---
BLUE='\033[1;34m'
BOLD='\033[1m'
CYAN='\033[1;36m'
GREEN='\033[1;32m'
PURPLE='\033[1;35m'
RED='\033[1;31m'
RESET='\033[0m'
YELLOW='\033[1;33m'

# --- Functions ---
print_ascii_banner() {
    echo -e "${PURPLE}============================================================${RESET}"
    echo -e "${BOLD}${BLUE}                    BASH PASSWORD GENERATOR ${RESET}"
    echo -e "${PURPLE}============================================================${RESET}"
}

print_ascii_ending() {
    local generated_password="$1"
    echo -e "${PURPLE}============================================================${RESET}"
    echo -e "${BOLD}${GREEN}Your Password:${RESET} ${BOLD}${CYAN}${generated_password}${RESET}"
    echo -e "${PURPLE}============================================================${RESET}"
}

# Unified message printing function (restored proper newlines with echo -e)
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
            echo -ne "${BOLD}${CYAN}[*] ${message_text} ${RESET}"
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
print_ascii_banner

# Prompt the user to enter the desired length for the password on the same line
print_message "status" "Please enter the length of the password (1-64):"

# Read the user's input and store it in the variable PASS_LENGTH.
read -r PASS_LENGTH

# Validate that input is a positive number and within the 1-64 character range
if ! [[ "$PASS_LENGTH" =~ ^[0-9]+$ ]] || [ "$((PASS_LENGTH))" -le 0 ] || [ "$((PASS_LENGTH))" -gt 64 ]; then
    print_message "error" "Please enter a valid number between 1 and 64."
    exit 1
fi

# Generate a random string using OpenSSL:
# 'openssl rand -base64 48': Generates 48 bytes of cryptographically secure
#                            random data and encodes it using Base64.
#                            Base64 characters include A-Z, a-z, 0-9, '+', '/', and '=' (padding).
#                            48 bytes of Base64 encoded data will result in 64 characters
#                            (48 * 8 bits / 6 bits per Base64 char = 64 characters before padding).
#
# 'cut -c1-$PASS_LENGTH': Takes the output from 'openssl rand' and cuts it.
#                        '-c1-$PASS_LENGTH' specifies to extract characters
#                        from the 1st position up to the length specified by PASS_LENGTH.
#                        This effectively truncates the 64-character base64 string
#                        to the user's desired password length.

GENERATED_PASSWORD=$(openssl rand -base64 48 | cut -c1-"$PASS_LENGTH")

# Print the final result inside the ending banner function cleanly
print_ascii_ending "$GENERATED_PASSWORD"

# --- End of Script ---