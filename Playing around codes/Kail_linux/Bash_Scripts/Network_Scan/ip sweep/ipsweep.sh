#!/bin/bash

# -------------------------------
# Network Scanner Script (Ping Sweep)
# Author: Wayne Stock
# Date:  5-20-25
# Description: Scans a /24 subnet for live hosts by pinging IPs from .1 to .254
# Usage: ./ipsweep.sh <subnet-prefix>  e.g., ./ipsweep.sh 192.168.1
# -------------------------------

# Loop through numbers 1 to 254 (these will be used as the last octet of the IP)
# $(seq 1 254) generates the list of numbers
for ip in $(seq 1 254); do

  # Ping the IP address one time (-c 1), using the subnet passed as the first argument ($1)
  # Example: if $1 is 192.168.1, this becomes 192.168.1.1, 192.168.1.2, etc.
  # Output of ping is piped to grep to search for "64 bytes" (indicating a successful reply)
  # The line is then passed through cut to extract the 4th space-separated field (the IP)
  # tr -d ":" removes the trailing colon from the IP
  ping -c 1 $1.$ip | grep "64 bytes" | cut -d " " -f 4 | tr -d ":" &

  # The '&' runs each ping command in the background so the loop can continue without waiting
  # This makes the scanning much faster, but we must be careful not to overwhelm the system
done
