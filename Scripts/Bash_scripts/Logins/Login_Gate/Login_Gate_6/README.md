# 🔐 Secure Gateway System (Level 6)

## 📝 Overview

The **Secure Gateway System** is a modular Bash-based security suite developed to protect sensitive data. Version 1.6 implements a **Decoupled Architecture**, where security logic is separated from user credentials and the protected data. This version introduces external vault authentication and automated audit logging.

## 📂 System Components

| File | Type | Description |
| :--- | :--- | :--- |
| **`Login_Gate_6.sh`** | Script | The core engine that handles input, hashing, and validation logic. |
| **`.vault.txt`** | Database | A hidden flat-file storing authorized `username:hash` pairs. |
| **`.login_attempts.log`** | Audit | A hidden log file recording timestamps, users, and success/fail status. |
| **`secret_data.txt`** | Resource | The protected manifest containing sensitive logistics data. |

## 🛠️ Security Features

* **SHA-256 Cryptography:** Passwords are never stored or compared in plain text. The system only validates cryptographic "fingerprints."
* **Brute-Force Protection:** Users are limited to **3 attempts** before a lockout is triggered.
* **Audit Trail:** Every interaction is timestamped and logged for forensic review.
* **Hidden File Logic:** Sensitive files (Vault and Logs) are prefixed with a dot (`.`) to keep them hidden from standard directory listings.

## 🚀 Installation & Setup

### 1. File Permissions

To ensure the system is secure, set the following permissions in your terminal:

```bash
# Make the main script executable
chmod +x Login_Gate_6.sh

# Protect the vault so only YOU can read/write it
chmod 600 .vault.txt

# Protect the secret data
chmod 600 secret_data.txt
