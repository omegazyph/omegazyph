# Login Gate 2 (Attempt Limiting)

## 📝 Overview

`Login_Gate_2.sh` is an upgraded security script that implements an **Attempt-Based Lockout**. Unlike the first version, this script gives the user three chances to enter the correct credentials before locking them out and terminating.

## 🛠️ Key Improvements

* **Looping Logic:** Uses a `while` loop with the `-gt` (greater than) operator to allow for retries.
* **Arithmetic Expansion:** Uses the `((variable--))` syntax to efficiently count down the remaining attempts.
* **Exit Codes:** Specifically uses `exit 0` for successful logins and `exit 1` for failures, allowing this script to be integrated into larger automated workflows.
* **Session Management:** Automatically clears the password line after entry to maintain a clean terminal interface.

## 🚀 Usage

### 1. Set Permissions

```bash
chmod +x Login_Gate_2.sh
