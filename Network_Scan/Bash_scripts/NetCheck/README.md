# NetCheck Security Scanner 🛡️

**Author:** omegazyph  
**Date:** January 4, 2026 (Updated: September 14, 2026)  
**Version:** v2.0.0  
**Platform:** Cross-platform (Linux / Git Bash on Windows)  

## 📖 Description

`NetCheck.sh` is a specialized network security utility designed to scan your local network, query the system Address Resolution Protocol (ARP) table, filter active IP and MAC address pairs, and generate an organized persistent text report.

It features clean ANSI terminal styling, modular functions, and smart path resolution to ensure reports are always saved directly inside the project directory.

## 🚀 Installation & Setup

1. **Create the script file:**

   nano NetCheck.sh

2. **Apply execution permissions:**

    Bashchmod +x NetCheck.sh

## 🛠️ Usage Instructions

Navigate to your project directory in your terminal (such as Git Bash or a Linux shell) and run the script[cite: 1, 2, 3]:Bash./NetCheck.sh

## 📊 Technical Details & Architecture Script Directory Anchoring:

* Utilizes $(dirname "${BASH_SOURCE[0]}") to ensure output files are reliably written to the script's folder regardless of your current working directory.

* Data Acquisition: Queries the operating system's ARP table via arp -a in a single optimized pass.  

* Data Filtering & Counting: Uses regular expressions via grep to isolate valid IPv4 addresses and compute active device counts.  

* Modular Logging Engine: Features a unified print_message function supporting color-coded status types (error, info, status, success, warning).  

## 📁 Project Structure

├── NetCheck.sh            # Main execution script

└── netcheck_report.txt    # Automatically generated scan log
