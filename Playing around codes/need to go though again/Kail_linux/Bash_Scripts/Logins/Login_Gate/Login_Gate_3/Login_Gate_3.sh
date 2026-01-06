#!/bin/bash

# ==============================================================================
# SCRIPT NAME:    Login_Gate_3.sh
# DESCRIPTION:    Level 3 Secure Gate: Unlocks a resource after authentication.
#                 Features: Retry limit, hidden input, and file verification.
# AUTHOR:         Wayne Stock
# DATE:           Jan 2, 2026
# VERSION:        1.3
# ==============================================================================

# --- Configuration Section ---
AUTHORIZED_USER="Wayne"
AUTHORIZED_PASS="12345"
SECRET_FILE="secret_data.txt"  # Resource protected by this gate

# --- Security Settings ---
ATTEMPTS_LEFT=3

# --- Main Login Loop ---
# This loop runs until ATTEMPTS_LEFT hits 0 or 'exit 0' is triggered.
while [[ $ATTEMPTS_LEFT -gt 0 ]]; do
    
    echo -e "\n=============================="
    echo "    ENCRYPTED ACCESS GATE"
    echo "=============================="
    
    # Prompt for identification
    read -p "Username: " entered_name
    
    # Prompt for credentials (-s prevents the password from appearing on screen)
    read -sp "Password: " entered_password
    echo "" # Cleanup terminal output after hidden input

    # --- Verification Logic ---
    # Checks if both name and password match the authorized keys
    if [[ "$AUTHORIZED_USER" == "$entered_name" && "$AUTHORIZED_PASS" == "$entered_password" ]]; then
        echo -e "\n[MATCH]: Credentials verified."
        echo "Accessing Resource: $SECRET_FILE"
        
        # --- Resource Verification ---
        # Checks if the file exists before attempting to read it
        if [[ -f "$SECRET_FILE" ]]; then
            echo "------------------------------------------------"
            cat "$SECRET_FILE"  # Reads the file to the terminal
            echo -e "\n------------------------------------------------"
        else
            # Error message if the file is missing from the directory
            echo "SYSTEM ERROR: Target file '$SECRET_FILE' is missing."
        fi
        
        # Authorize and terminate script successfully
        exit 0
    else 
        # Logic for incorrect credentials
        ((ATTEMPTS_LEFT--)) # Deduct one attempt
        echo -e "\n[DENIED]: Invalid credentials."
        
        # Warning for remaining attempts
        if [[ $ATTEMPTS_LEFT -gt 0 ]]; then
            echo "WARNING: System lockout in $ATTEMPTS_LEFT attempts."
        fi
    fi
done

# --- Lockdown Sequence ---
# Triggered only when the 'while' loop condition fails (0 attempts left).
echo -e "\n!!! SECURITY ALERT !!!"
echo "Maximum attempts reached. Lockdown initiated."
echo "I'm calling your mother... and the Sheriff."
exit 1