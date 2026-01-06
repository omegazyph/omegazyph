#!/bin/bash

# ==========================================================
# SCRIPT NAME:  NetCheck.sh
# AUTHOR:       omegazyph
# DATE:         January 4, 2026
# VERSION:      v1.0.0
# DESCRIPTION:  A security utility to scan the local network
#               and identify connected devices.
# ==========================================================

# --- COLORS ---
GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# --- INITIALIZATION ---
echo -e "${CYAN}===================================================="
echo "          NETCHECK SECURITY SCANNER v1.0.0        "
echo -e "====================================================${NC}"
echo "Scanning for active devices on your network..."
echo "Please wait (this may take a few seconds)..."
echo "----------------------------------------------------"

# --- THE SCAN ---
# 'arp -a' looks at the Address Resolution Protocol table
devices=$(arp -a)

if [ -z "$devices" ]; then
    echo -e "${RED}ERROR: No devices detected or ARP table is empty.${NC}"
    exit 1
fi

# --- THE REPORT ---
echo -e "${GREEN}IP ADDRESS        MAC ADDRESS           DEVICE NAME${NC}"
echo "----------------------------------------------------"

# Clean up the 'arp' output so it lines up in columns
arp -a | awk '{print $2, $4, $1}' | sed 's/(//g; s/)//g'

# --- SUMMARY ---
count=$(arp -a | wc -l)
echo "----------------------------------------------------"
echo -e "${CYAN}SCAN COMPLETE: $count devices found.${NC}"
echo -e "===================================================="