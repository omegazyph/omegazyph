#!/bin/bash

# ==============================================================================
# SCRIPT NAME:    Login_Gate_6.sh
# DESCRIPTION:    Level 6: External Vault Authentication System.
#                 Credentials are decoupled from logic and stored in .vault.txt.
# AUTHOR:         Wayne Stock
# DATE:           Jan 3, 2026
# VERSION:        1.6
# ==============================================================================

# --- File Resources ---
VAULT_FILE=".vault.txt"         # Secure Vault (Format -> user:hash)
SECRET_FILE="secret_data.txt"   # Protected Resource
LOG_FILE=".login_attempts.log"  # Audit Trail

# Security Settings
ATTEMPTS_REMAINING=3

# --- Pre-Flight Check ---
# Ensures the authentication database exists before proceeding.
if [[ ! -f "$VAULT_FILE" ]]; then
    echo "CRITICAL ERROR: Credentials vault ($VAULT_FILE) not found!"
    echo "Action Required: Create $VAULT_FILE with 'username:hash' format."
    exit 1
fi

# --- Helper Function: Logging ---
log_attempt() {
    local status=$1
    local user_tried=$2
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    echo "[$timestamp] User: $user_tried | Status: $status" >> "$LOG_FILE"
}

# --- Main Interaction Loop ---
while [[ $ATTEMPTS_REMAINING -gt 0 ]]; do
    
    echo -e "\n===================================="
    echo "    VAULT GATEWAY v1.6"
    echo "    Status: SECURE | Logging: ACTIVE"
    echo "===================================="
    
    read -p "Username: " entered_name
    read -sp "Password: " entered_password
    echo "" # Cleanup newline

    # 1. HASHING INPUT:
    # Convert password to SHA-256 hash for comparison.
    INPUT_HASH=$(echo -n "$entered_password" | sha256sum | awk '{print $1}')

    # 2. VAULT LOOKUP:
    # grep searches for the username at the start of the line (^).
    # cut uses the colon (:) as a delimiter to extract the second field (the hash).
    MATCHED_HASH=$(grep "^${entered_name}:" "$VAULT_FILE" | cut -d':' -f2)

    # 3. VERIFICATION LOGIC:
    # -n checks if MATCHED_HASH is not empty (user exists in vault).
    if [[ -n "$MATCHED_HASH" && "$MATCHED_HASH" == "$INPUT_HASH" ]]; then
        echo -e "\n[+] Access Granted! Welcome, $entered_name."
        log_attempt "SUCCESS" "$entered_name"
        
        # Display Resource
        if [[ -f "$SECRET_FILE" ]]; then
            echo "----------------------------------------"
            cat "$SECRET_FILE"
            echo -e "\n----------------------------------------"
        else
            echo "[-] Error: Secure file '$SECRET_FILE' missing."
        fi
        exit 0 
    else 
        # Failure logic
        ((ATTEMPTS_REMAINING--))
        echo -e "\n[!] Access Denied. Invalid User or Password."
        log_attempt "FAILED" "$entered_name"
        
        if [[ $ATTEMPTS_REMAINING -gt 0 ]]; then
            echo "System Lockout in $ATTEMPTS_REMAINING attempts."
        fi
    fi
done

# --- Lockdown Sequence ---
echo -e "\n[!!!] LOCKOUT TRIGGERED [!!!]"
log_attempt "LOCKOUT" "$entered_name"
echo "I'm calling your mother... and the Sheriff."
exit 1