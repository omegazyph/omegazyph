# Bash Password Generator (`Password_Generator.sh`)

An interactive, modular Bash script that generates cryptographically secure, random passwords of a user-specified length using OpenSSL and Base64 encoding.

## Author & Metadata

* **Author:** Omegazyph
* **Original Creation Date:** July 8, 2025
* **Last Updated:** September 15, 2026
* **Language:** Bash (`/usr/bin/env bash`)
* **Dependencies:** `openssl`, standard core utilities (`bash`, `cut`)

## Features

* **Cryptographically Secure Generation:** Leverages OpenSSL's pseudo-random number generator (`openssl rand`) rather than weak native shell random functions.

* **Diverse Character Set:** Uses Base64 encoding to produce a mix of uppercase letters (`A-Z`), lowercase letters (`a-z`), numbers (`0-9`), and symbols (`+`, `/`, `=`).

* **ANSI-Colored Terminal Interface:** Features custom color-coded status messages, error notifications, ASCII header bars, and formatted output.

* **Unified Input Validation:** Checks user input to ensure it is strictly numerical, greater than zero, and within safe boundaries (1 to 64 characters) before execution.

* **Clean Code Structure:** Avoids redundant loop mechanics and implements modular functions for clean maintainability.

## Prerequisites

Ensure that `openssl` is installed on your Linux, macOS, or WSL (Windows Subsystem for Linux) environment:

```bash
# Ubuntu / Debian / Parrot OS / Kali Linux
sudo apt update && sudo apt install openssl

# Verify installation
openssl version

Usage

    Clone or download the script into your target directory.

    Make the script executable:
    Bash

    chmod +x Password_Generator.sh

    Run the script:
    Bash

    ./Password_Generator.sh

    Follow the interactive prompt:

        Enter your desired password length when prompted (between 1 and 64 characters).

        The script will validate your input, generate the secure string, and present it inside a formatted banner.

Example Output
Plaintext

============================================================
                    BASH PASSWORD GENERATOR 
============================================================
[*] Please enter the length of the password (1-64): 24
============================================================
Your Password: 8Kx#v9LpQ2mZ!wR4yT7hBf1s
============================================================

Error Handling

The script validates input via arithmetic and regular expression matching:

    Non-numeric input (e.g., letters, blank input, special symbols): Triggers an error message ([X] Please enter a valid number between 1 and 64.) and exits with status code 1.

    Out-of-range input (e.g., 0, negative numbers, or lengths greater than 64): Triggers the same safety exit to prevent truncated or malformed output.

Code Structure Overview

    ANSI Color Variables: Global styling definitions for terminal coloring.

    print_ascii_banner(): Renders the starting visual border and title.

    print_ascii_ending(): Formats and displays the final generated password string.

    print_message(): A unified logging utility handling error, info, status, success, and warning message states.

    Main Process: Handles the interactive read call, regex validation, OpenSSL Base64 execution, and character truncation.
