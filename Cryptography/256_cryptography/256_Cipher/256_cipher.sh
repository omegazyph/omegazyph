#!/bin/bash

# ==============================================================================
# SCRIPT NAME:    256_cipher.sh
# DESCRIPTION:    Level 1 - Generates a SHA-256 hash from user input.
# AUTHOR:         Wayne Stock
# DATE:           Jan 3, 2026
# VERSION:        1.0
# ==============================================================================

# --- Visual Header ---
echo -e "\n===================================="
echo "      SHA-256 ENCRYPTION v1.1"
echo "===================================="

# --- User Input ---
# The -s flag hides the input (silent mode) so the password isn't visible on screen
read -sp "Enter the password to hash: " entered_password
echo -e "\n" # Adds a newline after the hidden input

# --- Hashing Process ---
# echo -n ensures no trailing newline is added to the string before hashing
# sha256sum calculates the hash
# awk '{print $1}' strips the trailing "-" character usually output by sha256sum
INPUT_HASH=$(echo -n "$entered_password" | sha256sum | awk '{print $1}')

# --- Results ---
echo "[*] Generated SHA-256 Hash:"
echo "----------------------------------------------------------------"
echo "$INPUT_HASH"
echo "----------------------------------------------------------------"

# Optional: Save to file for use with your cracker script
read -p "Would you like to save this to inputhash.txt? (y/n): " save_choice
if [[ "$save_choice" == "y" || "$save_choice" == "Y" ]]; then
    echo "$INPUT_HASH" > inputhash.txt
    echo "[SUCCESS] Hash saved to inputhash.txt"
fi

echo -e "\nProcess Complete."