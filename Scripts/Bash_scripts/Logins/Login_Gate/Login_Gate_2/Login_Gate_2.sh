#!/bin/bash

# ==============================================================================
# SCRIPT NAME:    Login_Gate_2.sh
# DESCRIPTION:    Advanced Login Gate with Attempt Limiting logic.
#                 Built upon Version 1.0 by adding a retry loop.
# AUTHOR:         Wayne Stock
# DATE:           Jan 2, 2026
# VERSION:        1.1
# USAGE:          ./Login_Gate_2.sh
# ==============================================================================

# --- Authorized Credentials ---
AUTHORIZED_USER="Wayne"
AUTHORIZED_PASS="12345"

# --- Attempt Counter ---
# We initialize the variable to track how many tries the user has left.
ATTEMPTS_REMAINING=3

echo "==================================="
echo "   SECURE LOGIN: ATTEMPT SYSTEM"
echo "==================================="

# --- Retry Loop ---
# This loop continues as long as the counter is greater than ( -gt ) zero.
while [[ $ATTEMPTS_REMAINING -gt 0 ]]; do
    
    echo -e "\nAttempts remaining: $ATTEMPTS_REMAINING"

    # Capture User Input
    read -p "Username: " entered_name
    
    # -s (silent) hides characters; -p (prompt) displays the text.
    read -sp "Password: " entered_password
    echo "" # Prints a newline after the silent password entry

    # --- Verification Logic ---
    if [[ "$AUTHORIZED_USER" == "$entered_name" && "$AUTHORIZED_PASS" == "$entered_password" ]]; then
        echo -e "\n[SUCCESS]: Access Granted. System Unlocked."
        exit 0 # Exit the script immediately on success
    else 
        # Decrement the counter if login fails
        ((ATTEMPTS_REMAINING--))
        
        if [[ $ATTEMPTS_REMAINING -gt 0 ]]; then
            echo -e "[ERROR]: Access Denied. Please try again."
        fi
    fi
done

# --- Lockdown Message ---
# This part only runs if the while loop finishes (meaning attempts reached 0).
echo "-----------------------------------"
echo "CRITICAL: Maximum login attempts exceeded."
echo "I'm Calling your Mother"
echo "-----------------------------------"

exit 1