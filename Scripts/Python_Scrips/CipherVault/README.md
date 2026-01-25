# CipherVault

CipherVault is a Zero-Trust, local-first password management system. It is designed to provide high-security credential storage using AES-256 encryption while maintaining a clean, readable command-line interface.

## Recent Updates

- **Immediate Generation Visibility:** The system now displays a newly generated password in bold yellow immediately so the user can copy it before it is encrypted.
- **Dynamic Window Scaling:** The interface now automatically detects terminal width and scales the data grid to fit the window size perfectly.
- **Enhanced Data Tracking:** Added dedicated fields for Website URLs and PIN codes for more comprehensive account management.
- **PEP 8 Compliance:** Refactored conditional logic to use standard Pythonic 'not' operators instead of direct boolean equality comparisons.

## Core Features

- **AES-256 Encryption:** Symmetric encryption via the Fernet protocol with keys derived through PBKDF2.
- **Separated Grid UI:** A structured table layout with row separators to ensure maximum readability.
- **Privacy Mode:** Passwords and PIN codes are masked in the "View All" mode to prevent shoulder-surfing.
- **Automated Binary Backups:** Every modification triggers a timestamped backup in the data/backups directory.

## Installation and Requirements

1. Ensure you have the required Python libraries installed:

   ```bash
   pip install cryptography rich

    Navigate to your project folder and execute the script:
    Bash

    python scripts/vault.py

Project Structure

scripts/vault.py: The main application logic.

data/vault_data.bin: The encrypted database (not to be uploaded to GitHub).

data/backups/: Storage for timestamped recovery files.

Author Information

Author: omegazyph

Date Created: 2026-01-25

Last Updated: 2026-01-25

---

### Final Sync for your GitHub

To keep your repository in sync with these final documentation changes, use these **non-shorthand** Git commands in your VSCode terminal:

1. **Stage all changes:**
   `git add --all`

2. **Commit with a descriptive message:**
   `git commit --message "docs: update README to include auto-sizing UI and password visibility features"`

3. **Push to GitHub:**
   `git push origin main`

**Is there anything else you would like to add to the documentation, or are we ready to call this project complete?**
