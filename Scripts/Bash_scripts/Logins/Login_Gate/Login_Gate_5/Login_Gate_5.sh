#!/bin/bash

# ==============================================================================
# SCRIPT NAME:    Login_Gate_5.sh
# DESCRIPTION:    Level 5: Cryptographic Login with Automated Audit Logging.
#                 Captures timestamps, usernames, and outcomes to a hidden log.
#                 Password 12345
# AUTHOR:         Wayne Stock
# DATE:           Jan 2, 2026
# VERSION:        1.5
# ==============================================================================

# --- Secure Credentials ---
AUTHORIZED_USER="Wayne"
STORED_HASH="5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5"

# --- Resources & Logs ---
SECRET_FILE="secret_data.txt"
LOG_FILE=".login_attempts.log"  # Hidden file (starts with a dot)

# Security Settings
ATTEMPTS_REMAINING=3

# --- Helper Function: Logging ---
# This modular function handles writing to the disk. 
# Usage: log_attempt "STATUS" "USERNAME"
log_attempt() {
    local status=$1
    local user_tried=$2
    # Generates a standard timestamp: YYYY-MM-DD HH:MM:SS
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    
    # Append the entry to the log file using '>>'
    echo "[$timestamp] User: $user_tried | Status: $status" >> "$LOG_FILE"
}

# --- Main Interaction ---
while [[ $ATTEMPTS_REMAINING -gt 0 ]]; do
    
    echo -e "\n===================================="
    echo "    ENCRYPTED GATEWAY v1.5"
    echo "    Audit Logging: ACTIVE"
    echo "===================================="
    
    read -p "Username: " entered_name
    read -sp "Password: " entered_password
    echo "" # Space for layout

    # Hashing Pipeline (SHA-256)
    INPUT_HASH=$(echo -n "$entered_password" | sha256sum | awk '{print $1}')

    # --- Verification & Audit Control ---
    if [[ "$AUTHORIZED_USER" == "$entered_name" && "$STORED_HASH" == "$INPUT_HASH" ]]; then
        echo -e "\n[+] Access Granted! Welcome back, $AUTHORIZED_USER."
        
        # Log the successful entry
        log_attempt "SUCCESS" "$entered_name"
        
        # Check for the secret resource
        if [[ -f "$SECRET_FILE" ]]; then
            echo "----------------------------------------"
            cat "$SECRET_FILE"
            echo -e "\n----------------------------------------"
        else
            echo "[-] Error: Secure resource '$SECRET_FILE' missing."
        fi
        
        exit 0 
    else 
        ((ATTEMPTS_REMAINING--))
        echo -e "\n[!] Access Denied. Hash mismatch."
        
        # Log the failed attempt
        log_attempt "FAILED" "$entered_name"
        
        if [[ $ATTEMPTS_REMAINING -gt 0 ]]; then
            echo "Lockout Warning: $ATTEMPTS_REMAINING tries left."
        fi
    fi
done

# --- Lockdown Protocol ---
echo -e "\n[!!!] LOCKOUT INITIATED [!!!]"
log_attempt "CRITICAL_LOCKOUT" "$entered_name"
echo "I'm calling your mother... and the Sheriff."

exit 1