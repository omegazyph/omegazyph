# ipsweep.sh

## Description

Scans a /24 subnet for live hosts by pinging IP addresses sequentially from `.1` to `.254`. Active hosts are logged to a text file and flagged in the terminal.

## Script Metadata

* **Author:** omegazyph
* **Created Date:** 2025-05-20
* **Updated Date:** 2026-09-13
* **Default Output Log:** `ip_list.txt`

## Usage

Run the script from your terminal by passing the target subnet prefix as an argument:

./ipsweep.sh (subnet-prefix)

Example (./ipsweep.sh 192.168.1)

## How It Works

    Displays an ASCII banner and checks whether a subnet prefix argument has been provided.

    Loops through host numbers from 1 to 254 to construct target IP addresses.

    Sends an ICMP ping packet to each target and checks for a valid response (64 bytes).

    If a host responds, the IP address is appended to ip_list.txt and a success message is displayed.
