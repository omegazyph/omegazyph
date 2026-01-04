# Encrypted Gateway (Bash)

A secure terminal-based login system featuring cryptographic hashing and input sanitization.

## 🚀 Features

- **Visual Password Masking:** Displays `****` instead of plain text or blank space.
- **SHA-256 Security:** Passwords are never stored in plain text; only hashes are compared.
- **Robust Sanitization:** Automatically trims accidental spaces and handles Windows/Linux line-ending differences.
- **Case-Insensitive:** Usernames can be entered in any case (e.g., `Wayne` or `wayne`).
- **Brute Force Protection:** Enforces a time delay between failed attempts and locks out after 3 failures.
- **Audit Logs:** Maintains a history of all attempts in `.login_attempts.log`.

## 🛠️ Setup

1. **The Vault:** Create a file named `.vault.txt` in the script directory.

2. **The Entries:** Add users using the format `username:hash`.
   *Example:*
   `wayne:5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5` (the hash for '12345')

3. **The Secret:** Create `secret_data.txt` to hold the data revealed upon successful login.

4. **Permissions:**

```bash
   chmod +x Login_Gate_8.sh
   chmod 600 .vault.txt
