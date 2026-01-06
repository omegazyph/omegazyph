# Debian/Ubuntu System Maintenance Script

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Important Notes](#important-notes)
- [Author](#author)
- [License](#license)

## Description

This Bash script automates common system maintenance tasks on Debian/Ubuntu-based Linux distributions. It ensures your system's package lists are up-to-date, upgrades all installed software (including core components like Bash), updates essential security tools (Exploit Database, Searchsploit, Nmap scripts), and performs system cleanup to free up disk space.

This script is a direct translation of a Python script designed for similar functionality.

## Features

- **Package List Update:** Refreshes the list of available packages from configured repositories (`sudo apt-get update`).

- **System Upgrade:** Performs a full system upgrade, handling dependencies and updating all installed software, including the Bash shell (`sudo apt-get dist-upgrade`).

- **Exploit Database Installation/Update:** Installs the `exploitdb` package and ensures it's up-to-date (`sudo apt-get install exploitdb`).

- **Searchsploit Database Update:** Updates the `searchsploit` database with the latest exploits and shellcodes (`searchsploit -u`).

- **Nmap Scripting Engine (NSE) Update:** Fetches the latest Nmap scripts for network scanning and security auditing (`sudo nmap --script-updatedb`).

- **Obsolete Package Removal:** Cleans up automatically installed packages that are no longer needed (`sudo apt-get autoremove --purge`).

- **Package Cache Cleanup:** Removes downloaded package archive files from the local cache (`sudo apt-get autoclean`).

- **Bash Version Verification:** Displays the currently installed Bash shell version.

## Prerequisites

- A Debian-based or Ubuntu-based Linux distribution.
- `sudo` access for running system-level commands.
- Internet connectivity for downloading updates and packages.
- `apt-get`, `searchsploit`, and `nmap` commands available on your system.

## Installation

1. **Save the script:**
    Save the code into a file, for example, `update_Kali.sh`.

    ```bash
    nano update_Kali.sh
    # Paste the script content and save
    ```

2. **Make it executable:**
    Grant execute permissions to the script:

    ```bash
    chmod +x update_Kali.sh
    ```

## Usage

To run the script, open your terminal and execute it with `sudo` privileges:

```bash
sudo ./update_Kali.sh

The script will provide output messages as it performs each step.

## Important Notes

    sudo: The script requires sudo privileges to perform most of its operations.

    Non-Interactive: The -y flag is used with apt-get commands, meaning the script will automatically confirm prompts without requiring user input.

    Searchsploit: The script correctly uses searchsploit -u for updating the database directly, correcting a common pattern seen in some scripts that incorrectly try to use apt-get for this.

## Author

    Wayne Stock

    Initial Date: 2024-01-21

    Last Update: 2025-07-07

## License

This project is licensed under the MIT License - see the LICENSE.md file for details (if you create one, otherwise specify your preferred license here).
