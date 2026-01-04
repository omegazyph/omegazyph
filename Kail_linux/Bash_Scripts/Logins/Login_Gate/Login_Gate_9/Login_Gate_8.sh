#!/bin/bash

# ==============================================================================
# SCRIPT NAME:    Login_Gate_8.sh
# DESCRIPTION:    Level 8: Hardened Security with ANSI UI, Masked Input (****),
#                 Case-Insensitive lookup, and Anti-Brute Force Delay.
# AUTHOR:         Wayne Stock
# DATE:           Jan 4, 2026
# VERSION:        1.8.2
# ==============================================================================

# --- ANSI UI Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# --- Resources ---
VAULT_FILE=".vault.txt"
SECRET_FILE="secret_data.txt"
LOG_FILE=".login_attempts.log"

# --- Security Parameters ---
ATTEMPTS_REMAINING=3
COOLDOWN_TIME=2 

# Ensure terminal settings are restored if the script is interrupted (Ctrl+C)
trap 'stty echo; echo -e "\n${RED}Program Terminated.${NC}"; exit' SIGINT SIGTERM

# --- Pre-Flight System Check ---
if [[ ! -f "$VAULT_FILE" ]]; then
    echo -e "${RED}[CRITICAL ERROR]: Vault file ($VAULT_FILE) not found.${NC}"
    exit 1
fi

# --- Logging Function ---
log_attempt() {
    local status=$1
    local user_tried=$2
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    echo -e "[$timestamp] User: $user_tried | Status: $status" >> "$LOG_FILE"
}

# --- Main Logic Loop ---
while [[ $ATTEMPTS_REMAINING -gt 0 ]]; do
    
    echo -e "\n${BLUE}====================================${NC}"
    echo -e "      ${BLUE}ENCRYPTED GATEWAY v1.8.2${NC}"
    echo -e "      Security Level: ${RED}MAXIMUM${NC}"
    echo -e "${BLUE}====================================${NC}"
    
    # --- Username Collection ---
    read -p "Username: " raw_name
    [[ -z "$raw_name" ]] && { echo -e "${RED}[!] Username required.${NC}"; continue; }

    # --- Masked Password Input ---
    # This loop reads one char at a time and prints an asterisk
    echo -n "Password: "
    raw_password=""
    while IFS= read -r -s -n1 char; do
        [[ -z "$char" ]] && break # Stop when Enter is pressed
        
        if [[ "$char" == $'\x7f' ]]; then # Handle Backspace
            if [[ ${#raw_password} -gt 0 ]]; then
                raw_password="${raw_password%?}" # Remove last char from variable
                echo -ne "\b \b" # Move back, overwrite with space, move back
            fi
        else
            raw_password+="$char"
            echo -n "*"
        fi
    done
    echo "" # Add newline after mask loop

    [[ -z "$raw_password" ]] && { echo -e "${RED}[!] Password required.${NC}"; continue; }

    # --- Sanitization & Normalization ---
    # xargs trims leading/trailing spaces
    entered_name=$(echo "$raw_name" | xargs)
    entered_password=$(echo "$raw_password" | xargs)

    # Convert to lowercase for case-insensitive lookup
    SEARCH_NAME="${entered_name,,}" 

    # Hash using printf to ensure NO hidden newlines are included in the hash
    INPUT_HASH=$(printf "%s" "$entered_password" | sha256sum | awk '{print $1}')

    # --- Vault Lookup ---
    # grep -i finds name regardless of case. ^ ensures we match start of line.
    MATCH_LINE=$(grep -i "^${SEARCH_NAME}:" "$VAULT_FILE")
    
    # Extract hash and strip Windows Carriage Returns (^M)
    MATCHED_HASH=$(echo "$MATCH_LINE" | cut -d':' -f2 | tr -d '\r' | xargs)

    # --- Verification ---
    if [[ -n "$MATCHED_HASH" && "$MATCHED_HASH" == "$INPUT_HASH" ]]; then
        echo -e "\n${GREEN}[SUCCESS]: Access Granted for $entered_name.${NC}"
        log_attempt "SUCCESS" "$entered_name"
        
        if [[ -f "$SECRET_FILE" ]]; then
            echo -e "${YELLOW}--- DECRYPTED DATA ---${NC}"
            cat "$SECRET_FILE"
            echo -e "${YELLOW}----------------------${NC}"
        fi
        exit 0 
    else 
        ((ATTEMPTS_REMAINING--))
        echo -e "\n${RED}[DENIED]: Invalid Credentials.${NC}"
        log_attempt "FAILED" "$entered_name"
        
        if [[ $ATTEMPTS_REMAINING -gt 0 ]]; then
            echo -e "${YELLOW}[!] Cooldown Active... ($ATTEMPTS_REMAINING tries left)${NC}"
            sleep $COOLDOWN_TIME
        fi
    fi
done

# --- Final Lockdown ---
echo -e "\n${RED}[!!!] LOCKOUT: Unauthorized Access Attempt [!!!]${NC}"
log_attempt "LOCKOUT" "$entered_name"
exit 1