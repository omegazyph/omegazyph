#!/bin/bash

# ==============================================================================
# SCRIPT NAME:    256_cipher.sh
# DESCRIPTION:    Level 1
#                 creates a hash in 256sha 
# AUTHOR:         Wayne Stock
# Started         jan 3, 2026
# DATE:           Jan 3, 2026
# Updated         Jan 3, 2026
# VERSION:        1.0
# ==============================================================================

echo -e "\n===================================="
    echo  "      256sha ENCRYPTION  v1.0"
    echo  "===================================="


read -p "Enter the password: " entered_password

INPUT_HASH=$(echo -n "$entered_password" | sha256sum | awk '{print $1}')

echo $INPUT_HASH
