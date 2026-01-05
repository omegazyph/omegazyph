#!/bin/bash

# ==============================================================================
# SCRIPT NAME:    vault_admin.sh
# DESCRIPTION:    Admin tool to securely add ONE user to the .vault.txt file.
# AUTHOR:         Wayne Stock
# DATE:           Jan 4, 2026
# VERSION:        1.0
# ==============================================================================

# --- Colors ---
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

VAULT_FILE=".vault.txt"

# Restore terminal if interrupted
trap 'stty echo; echo -e "\n${RED}Admin Cancelled.${NC}"; exit' SIGINT SIGTERM

echo -e "${YELLOW}====================================${NC}"
echo -e "      ${YELLOW}VAULT ADMINISTRATION${NC}"
echo -e "${YELLOW}====================================${NC}"

# 1. Username Input & Sanitization
read -p "New Username: " raw_name
[[ -z "$raw_name" ]] && { echo -e "${RED}[!] Error: Username required.${NC}"; exit 1; }

# Trim and lowercase to match the Gate's logic
new_name=$(echo "$raw_name" | xargs | tr '[:upper:]' '[:lower:]')

# 2. Duplicate Check
if grep -qi "^${new_name}:" "$VAULT_FILE" 2>/dev/null; then
    echo -e "${RED}[ERROR]: User '$new_name' already exists.${NC}"
    exit 1
fi

# 3. Secure Password Input (Masked)
echo -n "New Password: "
new_pass=""
while IFS= read -r -s -n1 char; do
    [[ -z "$char" ]] && break
    if [[ "$char" == $'\x7f' ]]; then
        if [[ ${#new_pass} -gt 0 ]]; then
            new_pass="${new_pass%?}"
            echo -ne "\b \b"
        fi
    else
        new_pass+="$char"
        echo -n "*"
    fi
done
echo "" # Newline after password input

[[ -z "$new_pass" ]] && { echo -e "${RED}[!] Error: Password required.${NC}"; exit 1; }

# 4. Hashing (Standardized to Gate logic)
# We use printf to ensure the hash is identical to what the Gate expects
USER_HASH=$(printf "%s" "$new_pass" | sha256sum | awk '{print $1}')

# 5. Save to Vault
echo "${new_name}:${USER_HASH}" >> "$VAULT_FILE"

echo -e "\n${GREEN}[SUCCESS]: User '$new_name' added to vault.${NC}"
echo -e "The user can now log in via Login_Gate_8.sh."