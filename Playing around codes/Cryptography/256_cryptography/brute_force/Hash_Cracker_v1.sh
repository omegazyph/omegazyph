#!/bin/bash

# ==============================================================================
# SCRIPT NAME:    Hash_Cracker_v1.sh
# DESCRIPTION:    Dictionary-based SHA-256 cracker. 
#                 Features: Clean string handling and dual-mode newline checking.
# AUTHOR:         Wayne Stock
# DATE:           Jan 3, 2026
# VERSION:        1.3
# ==============================================================================

# --- Visual Header ---
echo -e "\n===================================="
echo "      SHA-256 BRUTE_FORCE v1.3"
echo "===================================="

# --- Resources ---
# Configuration for input files
LIST="password_list.txt"
INPUT_HASH="inputhash.txt"

# --- Pre-Flight System Check ---
# Ensure required files exist before starting the process
if [[ ! -f "$LIST" ]]; then
    echo "[CRITICAL ERROR]: Wordlist ($LIST) missing."
    exit 1
fi

if [[ ! -f "$INPUT_HASH" ]]; then
    echo "[CRITICAL ERROR]: Target hash file ($INPUT_HASH) missing."
    exit 1
fi

# --- Preparation ---
# 1. Extract the hash (awk gets the first column)
# 2. Convert to lowercase (tr) to prevent case-match failures
TARGET_HASH=$(awk '{print $1}' "$INPUT_HASH" | tr '[:upper:]' '[:lower:]')

echo -e "[*] Starting Brute Force..."
echo -e "[*] Target Hash: $TARGET_HASH\n"

# --- Brute Force Loop ---
# 'IFS= read -r' prevents backslash escaping
# '|| [[ -n "$WORD" ]]' ensures the script processes the final line if it has no newline
while IFS= read -r WORD || [[ -n "$WORD" ]]; do
    
    # 1. SANITIZATION:
    # tr -d '\r' removes hidden Windows carriage returns
    # xargs trims any accidental leading/trailing spaces
    CLEAN_WORD=$(echo "$WORD" | tr -d '\r' | xargs)

    # Skip current iteration if the line is empty
    [[ -z "$CLEAN_WORD" ]] && continue

    # 2. DUAL-HASH GENERATION:
    # We check two variants because different tools generate hashes differently:
    #   - HASH_WITH_NL: Simulates 'echo "password"' (includes a newline)
    #   - HASH_NO_NL:   Simulates 'printf "password"' (no newline)
    HASH_WITH_NL=$(echo "$CLEAN_WORD" | sha256sum | awk '{print $1}')
    HASH_NO_NL=$(printf "%s" "$CLEAN_WORD" | sha256sum | awk '{print $1}')

    # 3. COMPARISON:
    # Check if either generated hash matches our target
    if [[ "$HASH_WITH_NL" == "$TARGET_HASH" || "$HASH_NO_NL" == "$TARGET_HASH" ]]; then
        echo -e "\n[SUCCESS] Match Found!"
        echo -e "------------------------------------------------"
        echo -e "Password: $CLEAN_WORD"
        echo -e "Hash:     $TARGET_HASH"
        echo -e "------------------------------------------------"
        exit 0
    fi

done < "$LIST"

# --- Termination ---
# Loop finished without finding a match
echo -e "\n[FAILURE] No match found in the wordlist."
exit 1