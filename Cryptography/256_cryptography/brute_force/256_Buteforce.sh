#!/bin/bash

# ==============================================================================
# SCRIPT NAME:    Login_Gate_7.sh
# DESCRIPTION:    Level 1
#                 this finds the word that macthes the hash
# AUTHOR:         Wayne Stock
# Started         jan 3, 2026
# DATE:           Jan 3, 2026
# Updated         Jan 3, 2026
# VERSION:        1.0
# ==============================================================================


# --- Resources ---
LIST="password_list.txt"
INPUT_HASH="inputhash.txt"
LOG_FILE=".login_attempts.log"


# --- Pre-Flight System Check ---
if [[ ! -f "$VAULT_FILE" ]]; then
    echo "[CRITICAL ERROR]: Wordlist  missing."
    exit 1
fi


# while loop