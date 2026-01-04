#!/bin/bash

# ==============================================================================
# SCRIPT NAME:    Hash_Cracker_v1.sh
# DESCRIPTION:    A robust SHA-256 dictionary cracker (Level 1).
#                 Handles Windows/Linux line endings and newline variations.
# AUTHOR:         Wayne Stock
# DATE:           Jan 3, 2026
# VERSION:        1.3
# ==============================================================================

# --- Visual Header ---
echo -e "\n===================================="
echo "      SHA-256 BRUTE_FORCE v1.3"
echo "===================================="

# --- Resources ---
LIST="password_list.txt"
INPUT_HASH="inputhash.txt"

# --- Pre-Flight System Check ---
if [[ ! -f "$LIST" ]]; then
    echo "[CRITICAL ERROR]: Wordlist ($LIST) missing."
    exit 1
fi

if [[ ! -f "$INPUT_HASH" ]]; then
    echo "[CRITICAL ERROR]: Target hash file ($INPUT_HASH) missing."
    exit 1
fi

# --- Preparation ---
# Read the target hash and convert to lowercase just in case
TARGET_HASH=$(awk '{print $1}' "$INPUT_HASH" | tr '[:upper:]' '[:lower:]')

echo -e "[*] Starting Brute Force..."
echo -e "[*] Target Hash: $TARGET_HASH\n"

# --- Brute Force Loop ---
# Use || [[ -n "$WORD" ]] to ensure the very last line is checked
while IFS= read -r WORD || [[ -n "$WORD" ]]; do
    
    # 1. CLEANUP: Remove hidden Windows (\r), tabs, and spaces
    CLEAN_WORD=$(echo "$WORD" | tr -d '\r' | xargs)

    # Skip empty lines
    [[ -z "$CLEAN_WORD" ]] && continue

    # 2. GENERATE BOTH HASH TYPES:
    # Some tools hash with a newline (echo), some without (printf). We check both.
    HASH_WITH_NL=$(echo "$CLEAN_WORD" | sha256sum | awk '{print $1}')
    HASH_NO_NL=$(printf "%s" "$CLEAN_WORD" | sha256sum | awk '{print $1}')

    # 3. DEBUG (Optional): Uncomment the line below to see every attempt
    # echo "Checking: [$CLEAN_WORD]"

    # 4. COMPARISON: Check against the target hash
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
echo -e "\n[FAILURE] No match found in the wordlist."
exit 1