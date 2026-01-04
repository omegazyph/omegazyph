# SHA-256 Hash Toolset (Level 1)

Created by **Wayne Stock** *Date: Jan 3, 2026*

## Description

This project consists of two Bash scripts designed to demonstrate the basics of cryptographic hashing and dictionary-based password recovery (cracking).

1. **256_cipher.sh**: A generator that takes a plain-text password and converts it into a SHA-256 hash.
2. **Hash_Cracker_v1.sh**: A recovery tool that compares a target hash against a list of common passwords to find a match.

---

## Files in this Project

* `256_cipher.sh` — The hashing tool.
* `Hash_Cracker_v1.sh` — The brute-force/dictionary tool.
* `password_list.txt` — Your dictionary of potential passwords.
* `inputhash.txt` — The target file where the hash is stored for cracking.

---

## Prerequisites

Before running the cracker, ensure you have a file named `password_list.txt` in the same directory containing one password per line.

---

## How to Use

### Step 1: Generate a Hash

Run the cipher script to create a target hash.

```bash
chmod +x 256_cipher.sh
./256_cipher.sh

Input your password and select 'y' to save it to inputhash.txt.
Step 2: Crack the Hash

Run the cracker script to see if the password exists in your wordlist.
Bash

chmod +x Hash_Cracker_v1.sh
./Hash_Cracker_v1.sh

Technical Details

    Algorithm: SHA-256

    Encoding: Handles both Linux (LF) and Windows (CRLF) line endings.

    Security: Uses silent input (read -s) to prevent passwords from being displayed in plain text during entry.
