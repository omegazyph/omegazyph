# Login Gate 5: Audit Logging System

## 📝 Overview

Level 5 moves the project into the realm of **Monitoring and Compliance**. This script not only gates access through SHA-256 cryptography but also maintains a persistent, hidden history of all interactions.

## 🛠️ New Technical Features

* **Helper Functions:** Introduced the `log_attempt` function to keep the main code clean and reusable.
* **Hidden Logging:** Uses a dot-file (`.login_attempts.log`) to keep the history hidden from standard `ls` commands.
* **Timestamping:** Utilizes the system `date` command to provide forensic data for every login attempt.
* **Persistent History:** Uses the `>>` append operator to ensure new logs are added to the bottom of the file without deleting previous history.

## 🚀 How to View the Audit Log

Because the log file is hidden, you need to use specific commands to see it:

1. **Find the file:** `ls -a`
2. **Read the history:** `cat .login_attempts.log`
3. **Watch logs in real-time:** `tail -f .login_attempts.log`

## 📋 Security Summary

* **Authentication:** SHA-256 Hash Comparison.
* **Accountability:** Full logging of Success, Failure, and Lockout events.
* **Integrity:** Validates presence of `secret_data.txt` before execution.

---
**Developer:** Wayne Stock  
**Security Level:** 5 (Audited Access Control)  
**Date:** January 2, 2026
