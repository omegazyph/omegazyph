# SHA-256 Hash Toolset (Level 1)

Created by **Wayne Stock** *Date: Jan 3, 2026*
Updated date *Jan 6, 2026

## Description

This project consists of two Bash scripts designed to demonstrate the basics of cryptographic hashing and dictionary-based password recovery (cracking).

1. **256_cipher.sh**: A generator that takes a plain-text password and converts it into a SHA-256 hash.

---

## Files in this Project

* `256_cipher.sh` — The hashing tool.
* `your_hash.txt` — The target file where the hash is stored for cracking.

---

## How to Use

### Step 1: Generate a Hash

Run the cipher script to create a target hash.

```bash
chmod +x 256_cipher.sh
./256_cipher.sh

Input your password and select 'y' to save it to your_hash.txt.

Technical Details

    Algorithm: SHA-256

    Encoding: Handles both Linux (LF) and Windows (CRLF) line endings.

    Security: Uses silent input (read -s) to prevent passwords from being displayed in plain text during entry.
