# CipherVault

**Date:** 2026-01-25
**Author:** omegazyph
**Updated:** 2026-01-25

## Description

CipherVault is a secure, Zero-Trust local password manager designed for Windows 11 Home. It utilizes AES-256 encryption via the `cryptography` library to ensure all sensitive data is protected. This project is built with an explicit, non-shorthand coding style to maintain strict compatibility with the Ruff linter.

---

## Features

* **Universal Exit Support:** You can type `exit` at any input prompt (Service, Website, Username, PIN, or Password) to cancel the operation and return to the menu.
* **Field-Specific Updates:** Update individual pieces of information (like just a PIN or just a URL) without having to re-enter the entire entry.
* **Dynamic UI:** Uses the `Rich` library to provide a clean, separated grid interface that automatically scales to your terminal's width.
* **A-Z Sorting:** Automatically organizes all vault entries alphabetically for easy navigation.
* **Automated Backups:** Every save operation creates a timestamped backup in the `data/backups` directory.

---

## File Structure

The program expects the following folder hierarchy:

```text
CipherVault/
│
├── scripts/
│   └── vault.py       # Main Python Script
│
└── data/
    ├── vault_data.bin # Encrypted Database
    └── backups/       # Timestamped Backup Files

Installation

To run this script on your Lenovo Legion, install the following requirements:
Bash

pip install cryptography rich

Usage

    Open the CipherVault folder in VSCode.

    Run the script: python scripts/vault.py.

    Enter your Master Encryption Key to unlock the vault.

    Follow the on-screen menu (1-7) to manage your credentials.

    Type exit at any time during an input prompt to cancel.

Developer Notes

    Style: No shorthand code is used to ensure maximum readability and linter compliance.

    Linter: Fully compatible with Ruff.

    Security: Static salt is used for PBKDF2 key derivation.
    