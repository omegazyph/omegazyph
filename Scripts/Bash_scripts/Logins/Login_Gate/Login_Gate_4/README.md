# Login Gate 4: Cryptographic Hashing

## 📝 Overview

Level 4 introduces **One-Way Hashing**. In this version, the script no longer knows what the password is; it only knows what the "fingerprint" (hash) of the password should look like. This is the industry standard for securing user credentials.

## 🛠️ Key Technical Features

* **SHA-256 Integration:** Uses the `sha256sum` utility to process user input into a 64-character hexadecimal string.
* **Data Sanitization:** Implements `awk` to clean up the output of the hashing tool, ensuring only the hash string is compared.
* **Non-Reversible Security:** Even if an attacker reads the script, they cannot easily reverse the hash to find the original password.
* **Exit Protocol:** Maintains strict exit codes (`0` for success, `1` for failure) for integration with other security modules.

## 🚀 How to Change the Password

To update the password in this script, you must generate a new hash:

1. Run this in your terminal: `echo -n "NewPasswordHere" | sha256sum`
2. Copy the long string of letters and numbers.
3. Replace the value in `STORED_HASH` with your new string.

## 📋 Requirements

* **Environment:** Kali Linux / Bash Shell.
* **Tools:** `sha256sum` and `awk` (standard in most Linux distros).

---
**Developer:** Wayne Stock  
**Security Level:** 4 (Cryptographic Verification)  
**Updated:** January 2, 2026
