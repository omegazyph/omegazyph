#!/bin/bash

# ==============================================================================
# SCRIPT NAME:    Login_Gate_8.sh
# DESCRIPTION:    Level 8: Hardened Security with ANSI UI, Input Sanitization,
#                 Case-Insensitive lookup, and Anti-Brute Force Delay.
# AUTHOR:         Wayne Stock
# DATE:           Jan 4, 2026
# VERSION:        1.8
# ==============================================================================

# --- ANSI UI Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color (Reset)

# --- Resources ---
VAULT_FILE=".vault.txt"
SECRET_FILE="secret_data.txt"
LOG_FILE=".login_attempts.log"

# Security Parameters
ATTEMPTS_REMAINING=3
COOLDOWN_TIME=2  # Seconds to wait after a failure

# --- Pre-Flight System Check ---
if [[ ! -f "$VAULT_FILE" ]]; then
    echo -e "${RED}[CRITICAL ERROR]: Vault missing. Security offline.${NC}"
    exit 1
fi

# --- Enhanced Logging Function ---
log_attempt() {
    local status=$1
    local user_tried=$2
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    local color=$NC

    case "$status" in
        "SUCCESS")           color=$GREEN ;;
        "FAILED")            color=$RED ;;
        "LOCKOUT TRIGGERED") color=$YELLOW ;;
    esac

    # Recording with ANSI codes allows 'cat' to show colors in the terminal later
    echo -e "[$timestamp] User: $user_tried | Status: ${color}${status}${NC}" >> "$LOG_FILE"
}

# --- Main Logic Loop ---
while [[ $ATTEMPTS_REMAINING -gt 0 ]]; do
    
    echo -e "\n${BLUE}====================================${NC}"
    echo -e "      ${BLUE}ENCRYPTED GATEWAY v1.8${NC}"
    echo -e "      Security Level: ${RED}MAXIMUM${NC}"
    echo -e "${BLUE}====================================${NC}"
    
    # --- Input Validation: Username ---
    read -p "Username: " entered_name
    if [[ -z "$entered_name" ]]; then
        echo -e "${RED}[!] ERROR: Username cannot be blank.${NC}"
        continue  # Restarts the loop without docking an attempt
    fi

    # --- Input Validation: Password ---
    read -sp "Password: " entered_password
    echo "" # Newline after hidden input
    if [[ -z "$entered_password" ]]; then
        echo -e "${RED}[!] ERROR: Password cannot be blank.${NC}"
        continue
    fi

    # --- Processing & Normalization ---
    # i changed it here
    #============================================================================
    # tr converts input to lowercase to make the login case-insensitive
    # SEARCH_NAME=$(echo "$entered_name" | tr '[:upper:]' '[:lower:]')
    # INPUT_HASH=$(echo -n "$entered_password" | sha256sum | awk '{print $1}')
    
    # grep -i performs a case-insensitive search in the vault
    # MATCHED_HASH=$(grep -i "^${SEARCH_NAME}:" "$VAULT_FILE" | cut -d':' -f2)
    #============================================================================
    
    # change it to 
    # ===========================================================================
    
    # 1. Trim accidental leading/trailing spaces from both inputs
    entered_name=$(echo "$entered_name" | xargs)
    entered_password=$(echo "$entered_password" | xargs)

    # 2. Convert name to lowercase for case-insensitive lookup
    SEARCH_NAME="${entered_name,,}" 

    # 3. Hash the "Clean" password using printf (No hidden newlines!)
    INPUT_HASH=$(printf "%s" "$entered_password" | sha256sum | awk '{print $1}')

    # 4. Pull the hash from the vault, stripping Windows ^M characters
    # Removing -F allows the ^ to work as an anchor (start of line)
    MATCH_LINE=$(grep -i "^${SEARCH_NAME}:" "$VAULT_FILE")
    
    # Pull the hash and strip that Windows ^M character
    MATCHED_HASH=$(echo "$MATCH_LINE" | cut -d':' -f2 | tr -d '\r')

    #============================================================================


    
    # --- Verification Sequence ---
    if [[ -n "$MATCHED_HASH" && "$MATCHED_HASH" == "$INPUT_HASH" ]]; then
        echo -e "\n${GREEN}[SUCCESS]: Authentication confirmed for $entered_name.${NC}"
        log_attempt "SUCCESS" "$entered_name"
        
        if [[ -f "$SECRET_FILE" ]]; then
            echo -e "${YELLOW}--- DECRYPTED RESOURCE ---${NC}"
            cat "$SECRET_FILE"
            echo -e "${YELLOW}--------------------------${NC}"
        fi
        exit 0 
    else 
        ((ATTEMPTS_REMAINING--))
        echo -e "\n${RED}[DENIED]: Credentials invalid.${NC}"
        log_attempt "FAILED" "$entered_name"
        
        if [[ $ATTEMPTS_REMAINING -gt 0 ]]; then
            echo -e "${YELLOW}[!] RATE LIMITING: System cooldown active...${NC}"
            # Rate limiting prevents rapid-fire automated password guessing
            sleep $COOLDOWN_TIME
            echo -e "Attempts remaining: $ATTEMPTS_REMAINING"
        fi
    fi
done

# --- Lockdown Sequence ---
echo -e "\n${RED}[!!!] LOCKOUT: SYSTEM SHUTDOWN [!!!]${NC}"
log_attempt "LOCKOUT TRIGGERED" "$entered_name"
exit 1