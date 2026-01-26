# CipherVault

**Date:** 2026-01-25
**Author:** omegazyph
**Updated:** 2026-01-25

## Description

CipherVault is a professional-grade, Zero-Trust local password manager built for Windows 11. It uses AES-256 encryption via the `cryptography` library to ensure that your credentials never leave your Lenovo Legion laptop. The codebase is written in a full, non-shorthand style to maintain 100% compliance with strict linters like Ruff.

---

## Features

* **Secure Update Generation:** When updating an existing entry, you now have the option to automatically generate a new 18-character secure password or type one in manually.
* **Universal Exit Support:** Type `exit` at any prompt (Service, Website, Username, PIN, or Password) to immediately cancel the action.
* **Granular Field Updates:** Change only what you need—pick between Website, Username, Password, or PIN without re-typing the entire record.
* **Dynamic Grid UI:** Features a separated grid interface powered by the `Rich` library that automatically adjusts to your VSCode terminal width.
* **Automated Backups:** Saves a timestamped binary copy of your vault in the `data/backups/` folder every time a change is made.
* **A-Z Sorting:** Automatically organizes all records alphabetically for quick searching and viewing.

---

## File Structure

The script is designed to run within the following folder hierarchy:

```text
CipherVault/
│
├── scripts/
│   └── vault.py       # Main Application
│
├── data/
│   ├── vault_data.bin # Encrypted Database
│   └── backups/       # Timestamped Backups
│
└── requirements.txt   # Project Dependencies

Installation & Setup

    Install Dependencies: Open your terminal in VSCode and run:
    Bash

    pip install -r requirements.txt

    Run Application:
    Bash

    python scripts/vault.py

Usage Instructions

    Master Key: Enter your secret key. This key is the only way to decrypt your data; do not lose it.

    Main Menu: Use keys 1-7 to navigate.

    Adding/Updating: When prompted for a password, you can select y to have the system generate a high-entropy 18-character string for you.

    Canceling: If you make a mistake, simply type exit to return to the main menu without saving changes.

Developer Notes

    Style: Strict adherence to non-shorthand Python logic.

    Linting: Optimized for Ruff to prevent unused variables and redundant boolean comparisons.

    Security: Employs PBKDF2 for key derivation with a static salt for local consistency.
