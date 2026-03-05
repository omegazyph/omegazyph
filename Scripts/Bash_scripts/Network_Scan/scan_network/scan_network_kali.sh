#!/bin/bash

# Wayne Stock - 2025-05-23
# Purpose: Only show unknown MACs on the local network

# Set the network interface to scan (e.g., eth0 or wlan0)
INTERFACE="eth0"

# File containing known MAC addresses (format: IP MAC LABEL)
KNOWN_MACS_FILE="known_macs.txt"

# Notify user the scan is starting on the specified interface
echo "[*] Scanning on interface $INTERFACE..."

# Initialize an array to hold known MAC addresses in uppercase for consistent comparison
KNOWN_MAC_LIST=()
while read -r _ MAC _; do
    # Convert the MAC address to uppercase
    MAC_CLEAN=$(echo "$MAC" | tr 'a-f' 'A-F')
    # Add the cleaned MAC to the known list
    KNOWN_MAC_LIST+=("$MAC_CLEAN")
done < "$KNOWN_MACS_FILE"

# Use arp-scan to scan the local network on the chosen interface
# Filter output lines that contain a valid MAC address pattern
sudo arp-scan --interface="$INTERFACE" --localnet | grep -Ei "([0-9a-f]{2}:){5}[0-9a-f]{2}" | while read -r IP MAC VENDOR; do
    # Convert the scanned MAC to uppercase for comparison
    MAC_UPPER=$(echo "$MAC" | tr 'a-f' 'A-F')

    # Attempt reverse DNS lookup to get hostname for the IP
    HOSTNAME=$(host "$IP" | awk '/domain name pointer/ {print $5}' | sed 's/\.$//')

    # If no hostname found, set to a default label
    [ -z "$HOSTNAME" ] && HOSTNAME="(no DNS name)"

    # Flag to check if MAC is known
    IS_KNOWN=false

    # Check each known MAC against the scanned MAC
    for KNOWN_MAC in "${KNOWN_MAC_LIST[@]}"; do
        if [[ "$MAC_UPPER" == "$KNOWN_MAC" ]]; then
            IS_KNOWN=true
            break
        fi
    done

    # If MAC is not known, print details about the unknown device
    if [ "$IS_KNOWN" = false ]; then
        echo "[!] UNKNOWN: $IP  $MAC  $HOSTNAME  $VENDOR"
    fi
done
