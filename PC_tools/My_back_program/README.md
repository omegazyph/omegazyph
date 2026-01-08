# 🛡️ OmegaZyph Legion Workstation Tools

A collection of custom Python-based automation tools designed for the **Lenovo Legion (Windows 11 Home)** environment. These tools provide system optimization, network diagnostics, and secure data synchronization to external storage.

---

## 🚀 Toolset Overview

| Script | Purpose | Key Feature |
| :--- | :--- | :--- |
| `legion_optimizer.py` | System Maintenance | SSD Trim, DNS Flush, Temp Cleanup |
| `network_ghost.py` | Connectivity Probe | Real-time Ping, Download, and Upload speeds |
| `legion_to_external_backup.py` | Data Redundancy | Incremental sync to LaCie (Z:) Drive |

---

## 🛠️ Installation & Setup

### 1. Requirements

Ensure your Legion has **Python 3.10+** installed. You will need to install the following dependencies via terminal:

bash
pip install psutil speedtest-cli

2.Environment Configuration

    Terminal: Best experienced in Windows Terminal with "Retro Terminal Effects" enabled.

    Colors: Optimized for Matrix Green (#00FF41) on a Transparent Black background.

    Editor: Developed in VS Code with Bash and Python extensions.

## 🖥️ Usage Instructions

System Optimization

Run as Administrator to ensure the SSD Trim and System Purge protocols have full access:
Bash

python legion_optimizer.py

Secure Backup

Ensure the LaCie (Z:) drive is connected before execution. The script performs an incremental sync, only copying files that have been modified.
Bash

python legion_to_external_backup.py

## 📂 Project Structure

    C:\Users\omega\OneDrive\Desktop\omegazyph -> Source Code & Projects

    Z:\Windows\Documents\Git hub projects\omegazyph_back_up -> Encrypted Backup Vault

## 📜 Credits & Metadata

    Author: omegazyph

    Last Updated: 2026-01-07

    Hardware: Lenovo Legion (Win 11 Home)

---

### How to use this in VSCode

1. In your `omegazyph` folder, click the **New File** icon.
2. Name it exactly `README.md`.
3. Paste the code above into the file.
4. **Pro Tip:** In VSCode, press **Ctrl + Shift + V** to see a "Preview" of how the markdown looks. It will render the tables and bold text beautifully.
