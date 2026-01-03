#!/bin/bash

# ==============================================================================
# SCRIPT NAME:    Login_Gate_4.sh
# DESCRIPTION:    Level 4 Secure Gate: Password Hashing (SHA-256) implementation.
#                 Verifies hashed input against a stored fingerprint before 
#                 displaying protected file contents.
# AUTHOR:         Wayne Stock
# DATE:           Jan 2, 2026
# VERSION:        1.4
# ==============================================================================

# --- Secure Credentials ---
AUTHORIZED_USER="Wayne"

# SHA-256 fingerprint for "12345"
# Note: Storing hashes is safer than storing plain-text passwords.
STORED_HASH="5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5"

# Target Resource
SECRET_FILE="secret_data.txt"

# Security Settings
ATTEMPTS_REMAINING=3

# --- Main Login Loop ---
while [[ $ATTEMPTS_REMAINING -gt 0 ]]; do
    
    echo -e "\n===================================="
    echo "    ENCRYPTED GATEWAY (Level 4)"
    echo "    Security Status: ACTIVE"
    echo "===================================="
    
    read -p "Username: " entered_name
    read -sp "Password: " entered_password
    echo "" # Cleanup after silent input

    # --- Hashing Pipeline ---
    # 1. echo -n : Sends password without a newline (very important for correct hashing).
    # 2. sha256sum : Generates the 64-character hash.
    # 3. awk '{print $1}' : Extracts only the hash, removing the trailing dash/filename.
    INPUT_HASH=$(echo -n "$entered_password" | sha256sum | awk '{print $1}')

    # --- Cryptographic Verification ---
    # We compare the generated hash from the user to our stored fingerprint.
    if [[ "$AUTHORIZED_USER" == "$entered_name" && "$STORED_HASH" == "$INPUT_HASH" ]]; then
        echo -e "\n[+] Access Granted! Fingerprint match confirmed."
        
        # Verify resource existence
        if [[ -f "$SECRET_FILE" ]]; then
            echo "Decrypted Content of $SECRET_FILE:"
            echo "----------------------------------------"
            cat "$SECRET_FILE"
            echo -e "\n----------------------------------------"
        else
            echo "[-] Error: Resource $SECRET_FILE missing from directory."
        fi
        
        exit 0 # Success exit
    else 
        ((ATTEMPTS_REMAINING--))
        echo -e "\n[!] Access Denied: Invalid Username or Password Hash."
        
        if [[ $ATTEMPTS_REMAINING -gt 0 ]]; then
            echo "System Lockout in $ATTEMPTS_REMAINING attempts."
        fi
    fi
done

# --- Lockdown Sequence ---
echo -e "\n[!!!] CRITICAL SECURITY BREACH [!!!]"
echo "Maximum attempts reached. Sheriff has been notified."
echo "I'm calling your mother... and the Sheriff."
exit 1 # Failure exit