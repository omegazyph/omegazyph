#!/bin/bash

# ==============================================================================
# SCRIPT NAME:    256_cipher.sh
# DESCRIPTION:    Generates a SHA-256 hash from user input and saves it to a file.
# AUTHOR:         Wayne Stock
# DATE:           Jan 3, 2026
# VERSION:        1.2
# ==============================================================================

# --- Visual Header ---
# Clear the screen or just provide a clean start for the user
echo -e "\n===================================="
echo "      SHA-256 HASH GENERATOR v1.0"
echo "===================================="

# --- User Input ---
# -s: Silent mode (password characters won't show on screen)
# -p: Prompt message
read -sp "Enter the password to hash: " entered_password
echo -e "\n" # Adds a newline for visual spacing after hidden input

# --- Hashing Process ---
# We use echo without '-n' here to ensure the resulting hash matches 
# the format expected by the cracker script (includes trailing newline).
INPUT_HASH=$(echo "$entered_password" | sha256sum | awk '{print $1}')

# --- Results Display ---
echo "[*] Generated SHA-256 Hash:"
echo "----------------------------------------------------------------"
echo "$INPUT_HASH"
echo "----------------------------------------------------------------"

# --- Save to File ---
# Prompt the user if they want to export this hash for the Cracker script
read -p "Would you like to save this to your_hash.txt? (y/n): " save_choice

if [[ "$save_choice" == "y" || "$save_choice" == "Y" ]]; then
    # Write the hash string to your_hash.txt, overwriting any previous content
    echo "$INPUT_HASH" > your_hash.txt
    echo -e "\n[SUCCESS] Hash saved to your_hash.txt"
else
    echo -e "\n[*] Hash was not saved."
fi

echo -e "Process Complete.\n"