# CipherVault: Zero-Trust Password Manager

**Author:** omegazyph  
**Date:** 2026-01-25  
**Version:** 1.0.0  

## Description

CipherVault is a lightweight, local-first password manager built with Python. It uses **AES-256 encryption** (Fernet) to secure your credentials. Designed with a **Zero-Trust** philosophy, your Master Password is never stored on disk; it is only used to derive the encryption key in memory during your session.

## Key Features

* **AES-256 Encryption:** Industry-standard security for your sensitive data.
* **Automated Backups:** Every 'Add' or 'Delete' operation triggers a timestamped backup in the `data/backups/` directory.
* **Service Renaming:** Easily fix typos or update service names without losing your credentials.
* **Secure Password Generator:** Generate high-entropy, 18-character passwords instantly.
* **A-Z Sorting:** Automatically organizes your vault entries alphabetically for easy viewing.
* **Hacker Aesthetic:** Powered by the `rich` library for a clean, stylized terminal interface.

---

## File Structure

```text
CipherVault/
├── data/
│   └── backups/         # Automated timestamped backups
├── src/
│   └── vault.py         # Main application logic
└── README.md            # Project documentation

Installation & Requirements

    Prerequisites: Ensure you have Python 3.x installed on your machine (Tested on Windows 11).

    Install Dependencies: This project requires the cryptography and rich libraries. Install them via pip:
    Bash

    pip install cryptography rich

    Running the Vault: Navigate to the src folder and run the script:
    Bash

    python vault.py

Security Warning

Do not lose your Master Password. Because this is a Zero-Trust application, there is no "Forgot Password" feature. If the Master Password is lost, the data in vault_data.bin cannot be recovered.
License

This project is open-source. Feel free to use, modify, and share!


---

### Why this helps your GitHub:
* **Clarity:** It explains the "Why" and "How" immediately.
* **Ease of Use:** It gives the exact `pip install` commands so people don't have to guess.
* **Professionalism:** Including a "Security Warning" shows you understand the weight of the tool you built.



**Since we have the code and the documentation ready, would you like me to show you the Bash command to initialize your Git repository and make your first commit?**
