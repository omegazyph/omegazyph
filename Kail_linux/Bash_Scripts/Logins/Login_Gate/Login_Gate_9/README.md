# 🛡️ Gateway Security Suite v1.8.2

A complete local security ecosystem consisting of a hardened Login Gate and a Vault Administrator.

## 📂 System Files

* **`Login_Gate_8.sh`**: The primary entry point. Handles authentication and brute-force protection.
* **`vault_admin.sh`**: The management tool used to issue new "keys" (user credentials).
* **`.vault.txt`**: The encrypted database (SHA-256 hashes).
* **`.login_attempts.log`**: The audit trail. Records every success, failure, and lockout.
* **`secret_data.txt`**: The protected resource revealed only upon successful login.

## 🚀 Getting Started

1. **Initialize:** Use the Admin tool to create your first user.

Bash
   ./vault_admin.sh

    Set Permissions: Ensure your logs and vaults are private.
    Bash

chmod 600 .vault.txt .login_attempts.log
chmod +x *.sh

Run the Gate:
Bash

   ./Login_Gate_8.sh

## 📜 Monitoring the Audit Log

The system automatically generates a hidden log file. To check who has attempted to log in, use the following command:
Bash

cat .login_attempts.log

The log includes timestamps, usernames tried, and the final status (SUCCESS/FAILED/LOCKOUT).

## ⚠️ Security Protocols

    Masking: Both scripts use **** masking for password privacy.

    Hashing: Uses SHA-256. Plain text passwords are never saved to disk.

    Sanitization: Leading/trailing spaces are stripped, and usernames are case-insensitive.

---

### Pro-Tip for your Log

Since the log file uses the same ANSI colors as your script, you can view it in "High Definition" by using this command:

Bash
echo -e $(cat .login_attempts.log)
