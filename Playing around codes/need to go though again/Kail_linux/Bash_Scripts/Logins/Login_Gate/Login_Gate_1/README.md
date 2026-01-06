# Login Gate 1

## 📝 Project Overview

`Login_Gate_1.sh` is a fundamental security script designed for Bash environments. It acts as a credential validator, requiring a specific username and password before allowing a user to proceed within a script or system.

## 🛠️ Technical Features

* **Silent Password Entry:** Utilizes the `-s` flag in the `read` command to prevent the password from being displayed on the screen while the user types (preventing "shoulder surfing").
* **Conditional Logic:** Employs a double-bracket `[[ ... ]]` test for high-reliability string comparison.
* **Formatted Output:** Uses the `echo -e` flag to manage vertical spacing and provide a cleaner user interface in the terminal.

## 🚀 How to Use

### 1. Set Permissions

Before running the script in your Linux/Kali environment, you must make it executable:

```bash
chmod +x Login_Gate_1.sh
