# 🔐 Password Manager V3.1

## 📝 Overview

**Password Manager V3.1** is a secure, graphical desktop application designed by **omegazyph**. It provides a robust solution for storing and managing sensitive credentials using **AES-256 bit encryption**. By utilizing the `cryptography` library's Fernet implementation, it ensures that your data remains private and unreadable to anyone without the specific encryption key.

## ✨ Features

* **Tkinter GUI:** A clean, dark-themed user interface for ease of use.
* **Master Password Protection:** A security gate that requires a master password (default: `12345`) before the application opens.
* **Fernet Encryption:** Symmetric encryption that turns your site credentials into secure ciphertext.
* **Key Management:** Dedicated logic to generate and protect your unique `key.key` file.
* **Smart Sorting:** Automatically organizes your saved entries alphabetically by site name.
* **Masked Entry:** Passwords are hidden with asterisks (`*`) during input to prevent "shoulder surfing."

## 📂 File Structure

| File | Importance | Description |
| :--- | :--- | :--- |
| **`password_manager_v3.py`** | **Critical** | The main application code and logic. |
| **`key.key`** | **High** | The unique encryption key. **Do not lose this!** |
| **`passwords.txt`** | **Medium** | Stores your encrypted site data. |

## 🚀 How to Install & Run

1. **Install Dependencies:**
   Ensure you have the `cryptography` library installed:

bash
   pip install cryptography

    Run the Application:
    Bash

    python3 password_manager_v3.py

## ⚠️ Important Security Note

The key.key file is the only way to decrypt your passwords. It is highly recommended to keep this file in a separate directory or on a secure backup drive. If the key file is deleted or overwritten, any existing data in passwords.txt will be permanently lost.

Author: omegazyph

Updated: 2026-01-05

Version: 3.1
