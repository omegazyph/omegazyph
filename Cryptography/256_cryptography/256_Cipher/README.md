# 🔐 Secure Gateway System (Level 7)

## 📝 Overview

The **Secure Gateway System** is a modular Bash-based security suite developed to protect sensitive data. Version 1.7 represents the "Hardened" edition, featuring **Defensive Programming** techniques, external vault authentication, and automated audit logging. This system is designed to be resilient against both human error and automated brute-force attacks.

## 📂 System Architecture

To maintain a "Separation of Concerns," the system is divided into four distinct files:

| File | Type | Description |
| :--- | :--- | :--- |
| **`Login_Gate_7.sh`** | Script | The core logic engine featuring Rate Limiting and an ANSI-colored UI. |
| **`256_cipher.sh`** | Tool | Level 1 utility to generate SHA-256 hashes for the vault. |
| **`.vault.txt`** | Database | A hidden store for authorized `username:hash` pairs. |
| **`.login_attempts.log`** | Audit | A persistent, color-coded history of all access attempts. |
| **`secret_data.txt`** | Resource | The protected content (Trucking Manifest for Van, TX). |

## 🛠️ Advanced Security Features

* **Rate Limiting (Anti-Brute Force):** Implements a mandatory 2-second `sleep` delay after a failed login to stop rapid-fire automated guessing.
* **Input Sanitization:** Checks for empty strings (`[[ -z ]]`) to ensure fields are not empty before the system wastes CPU cycles on hashing.
* **SHA-256 Cryptography:** Passwords are never stored in plain text; only cryptographic fingerprints are compared.
* **Case-Insensitive Normalization:** Converts input to lowercase using `tr`, preventing login failure due to simple capitalization errors.
* **Forensic Logging:** Records every entry with ANSI color-coding (Green for Success, Red for Failure, Yellow for Lockouts).

## 🚀 Installation & Setup

### 1. File Permissions

Secure the environment by running the following commands in your terminal:

(bash)

## Grant execution rights to the scripts

chmod +x Login_Gate_7.sh
chmod +x 256_cipher.sh

## Restrict the vault so only the owner can read it

chmod 600 .vault.txt

## Secure the sensitive manifest

chmod 600 secret_data.txt

## 2.Execution

Launch the gateway using the following command:
Bash

./Login_Gate_7.sh

## 📋 Security Philosophy

The goal of Level 7 is Defensive Programming. By controlling the speed of the login process and validating input before processing, the script protects underlying system resources from unnecessary load and common attack vectors. This "slow-down" approach (Rate Limiting) makes automated dictionary attacks practically impossible by significantly increasing the "time-cost" for the attacker.

## 📊 Administrative Monitoring

To review the audit trail or watch login attempts in real-time, use:
Bash

## View the full history

cat .login_attempts.log

## Monitor attempts live as they happen

tail -f .login_attempts.log

Developer: Wayne Stock

Version: 1.1 (Hardened Security)

Date: January 3, 2026
