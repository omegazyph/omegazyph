# CipherVault: Secure Credential Manager

**Project Folder:** `CipherVault_Project`  
**Author:** omegazyph  
**Last Updated:** 2026-01-26  
**System Requirements:** Windows 11 / Lenovo Legion Laptop / Python 3.x

---

## [ DESCRIPTION ]

CipherVault is a high-security, Advanced Encryption Standard 256 encrypted credential manager designed for local use on Windows 11. It features a custom "hacker-style" graphical user interface optimized for the full-screen display of a Lenovo Legion laptop. The program allows for the secure storage of service names, website addresses, usernames, passwords, personal identification numbers, and dual two-factor authentication backup codes.

---

## [ PROJECT STRUCTURE ]

CipherVault_Project/
│
├── scripts/
│   └── vault_hacker_gui.pyw      # Main Graphical User Interface Application (Python)
│
├── data/
│   ├── vault_data.bin            # Encrypted Binary Data (Advanced Encryption Standard 256)
│   └── backups/                  # Automated timestamped backup files
│
└── README.md                     # Documentation

---

## [ KEY FEATURES ]

    Advanced Encryption Standard 256 Encryption: Utilizes the Fernet symmetric encryption library and the Password-Based Key Derivation Function 2 for high security.

    Full-Screen Optimization: Columns are weighted to prioritize Service, Website, and Username visibility while keeping security fields compact.

    Numeric Four-Digit Personal Identification Number Generation: Automatically generates random four-digit numeric numbers if the field is left blank during creation or editing.

    Secure Password Generation: High-entropy password generation (twenty or more characters including symbols).

    Automatic Backups: Every time the vault is saved, a timestamped copy is placed in the data/backups/ directory for system recovery.

    Deep Integration: Native "Open Website Address" functionality and "Copy to Clipboard" tools for generated passwords.

---

## [ INSTALLATION AND SETUP ]

    Install Dependencies: Ensure you have the cryptography library installed via the terminal command:
    Bash

    pip install cryptography

    Execution: Run the application using Python:
    Bash

    python scripts/vault_hacker_gui.pyw

    Note: The .pyw file extension is used to prevent the Windows command prompt from appearing in the background.

---

## [ OPERATIONAL LOGIC ]

    Authentication: The Master Key is never stored on the system. If the master key is lost, the data cannot be recovered.

    Automatic Generation: To trigger the automatic generator for Passwords or Personal Identification Numbers:

        Click the ADD_NEW_ENTRY or EDIT_EXISTING_ENTRY button.

        Leave the input field blank (or clear the existing text in Edit mode).

        Click the OK button. The system will populate the field with a fresh secure string.

    Masking: The main grid masks sensitive data with asterisks to prevent unauthorized viewing. Use the VIEW_RECORD_DATA button to see the raw information.
