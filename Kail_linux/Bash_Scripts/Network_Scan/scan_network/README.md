# Unknown Device Network Scanner

**Author:** Wayne Stock  
**Date:** 2025-05-22

---

## Overview

This Bash script scans your local network on a specified interface (e.g., `eth0` or `wlan0`) and reports only devices whose MAC addresses are **not** listed in your known devices file (`known_macs.txt`). It helps you identify unknown or unauthorized devices on your network.

---

## Features

- Uses `arp-scan` to detect all devices connected to your local network.
- Compares scanned MAC addresses against a whitelist (`known_macs.txt`).
- Displays only unknown devices with their IP address, MAC address, hostname (if available), and vendor.
- Automatically normalizes MAC addresses to uppercase for accurate matching.
- Performs reverse DNS lookup to show device hostnames when possible.

---

## Requirements

- Linux system with Bash shell
- `arp-scan` installed (`sudo apt-get install arp-scan` on Debian/Ubuntu/Kali)
- `host` command available (usually part of the `bind-utils` or `dnsutils` package)

---

## Setup

1. Clone or copy the script file to your machine.
2. Create a `known_macs.txt` file in the same directory.  
   Format each line as:  
3. Make sure the script is executable:  
```bash
chmod +x network_scan.sh
