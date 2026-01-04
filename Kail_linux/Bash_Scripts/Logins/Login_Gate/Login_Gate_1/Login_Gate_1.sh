#!/bin/bash

# ==============================================================================
# SCRIPT NAME:    Login_Gate_1.sh
# DESCRIPTION:    A secure command-line login gate with masked password input.
# AUTHOR:         Wayne Stock
# DATE:           Jan 2, 2026
# VERSION:        1.0
# USAGE:          ./Login_Gate_1.sh
# ==============================================================================

# --- Credentials (The Key) ---
# These variables store the authorized user information.
CORRECT_USER="Wayne"
CORRECT_PASS="12345"

# --- User Entry ---
# 'read -p' is used to display the prompt and take input on the same line.
echo "-----------------------------------"
echo "      SECURE SYSTEM ACCESS"
echo "-----------------------------------"

read -p "Username: " entered_name

# '-s' (silent) hides the password characters for security.
# '-p' allows the text prompt.
read -sp "Password: " entered_password

# --- Logic Check ---
# The 'if' statement uses '[[' for advanced string comparison.
# '&&' ensures BOTH the username AND the password must match exactly.
if [[ "$CORRECT_USER" == "$entered_name" && "$CORRECT_PASS" == "$entered_password" ]]; then
    # '-e' enables the interpretation of backslash escapes like '\n' (newline).
    echo -e "\n\n[SUCCESS]: Access Granted. Welcome, $CORRECT_USER."
else 
    echo -e "\n\n[ERROR]: Access Denied. Invalid credentials."
    # Exit with a non-zero status to indicate failure
    exit 1
fi

echo "-----------------------------------"