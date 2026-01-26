# CipherVault: Multi-Interface AES-256 Password Manager

**Date:** 2026-01-25
**Author:** omegazyph
**Updated:** 2026-01-25

## Project Overview

CipherVault is a localized, high-security credential management system built for Windows 11. It utilizes industry-standard AES-256 encryption via the Fernet protocol. This project provides two distinct ways to access your secure data: a high-efficiency **Terminal Interface** and a stealth **Hacker GUI**.

---

## File Structure

Your project folder on your Lenovo Legion should be organized as follows:

CipherVault_Project/
│
├── scripts/
│   ├── vault.py              # Terminal-based Manager (requires 'rich')
│   └── vault_hacker_gui.pyw  # Stealth GUI Manager (Windowless)
│
├── data/
│   ├── vault_data.bin        # Encrypted Database (Shared)
│   └── backups/              # Automated Binary Backups
│
├── Launch_Vault.vbs          # Silent Launcher for the GUI
└── README.md                 # Project Documentation

## Component Details

1. Terminal Manager (vault.py)

    Interface: Command-line based with a color-coded grid.

    Best Use: Rapid data entry while working inside VSCode.

    Requirement: Must be run via python scripts/vault.py.

2. Hacker GUI Pro (vault_hacker_gui.pyw)

    Interface: Tkinter-based "Matrix" aesthetic (Green on Black).

    Key Features: * Windowless: Does not open a CMD window when launched via VBScript.

        Auto-Resize: Columns grow automatically to fit long URLs or usernames.

        Secure Clipboard: Copies passwords and automatically wipes the clipboard after 30 seconds.

        Visual Management: Dedicated buttons for Add, View, Copy, and Delete.

## Setup & Requirements

Dependencies

Install the required Python libraries using the VSCode terminal:
Bash

pip install cryptography rich

Silent Launching (GUI)

To run the GUI without the black command prompt window popping up:

    Double-click the Launch_Vault.vbs file located in the root folder.

    This script calls pythonw.exe to run the .pyw logic in the background.

## Security Protocol

    Master Key: Your data is only as secure as your Master Key. If lost, the vault_data.bin cannot be recovered.

    Zero-Trust: No data is sent to the cloud. All encryption happens locally on your hardware.

    Entropy: For maximum security, use the "Auto-Gen" feature when adding passwords to ensure high-entropy strings.

    Backups: Every time you save, a new backup is created in data/backups/. Periodically clear out old backups to save space.

## Instructions for Use

    Adding: Provide the service name, URL, and username. Leave the password blank to generate a 20-character secure key.

    Copying: Select a row and hit COPY_PASS. You have 30 seconds to paste it before it is wiped from memory.

    Deleting: Select a row and hit DELETE_ENTRY. A confirmation dialog will appear to prevent accidental loss.
    