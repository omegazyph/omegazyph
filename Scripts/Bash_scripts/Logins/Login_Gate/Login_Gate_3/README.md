# Login Gate 3: Resource Protection System

## 📝 Overview

`Login_Gate_3.sh` is a security-oriented Bash script that acts as a gatekeeper for a specific data file. It combines credential validation with file-system checks to ensure only authorized users can view sensitive information.

## 🛠️ Key Technical Features

* **Defensive Programming:** Includes a check (`-f`) to verify the existence of the secret file, preventing "File Not Found" errors.
* **Security-Conscious Input:** Uses `read -sp` to ensure passwords are not visible to bystanders.
* **Dynamic Feedback:** Keeps the user informed of how many attempts remain before a system lockout.
* **Exit Codes:** Uses `exit 0` for success and `exit 1` for failure, making it compatible with other Linux automation tools.

## 🚀 Usage

### 1. Create the Secret File

The gate needs something to protect. Create a file named `secret_data.txt` in the same folder:

```bash
echo "Top Secret: The password is guest" > secret_data.txt
