# NetCheck Security Scanner 🛡️

**Author:** omegazyph  
**Date:** January 4, 2026  
**Version:** v1.2.0  
**Platform:** Parrot OS / Linux  

## 📖 Description

`NetCheck.sh` is a specialized network utility built for the **Parrot Security OS** environment. It audits the local network by querying the kernel's neighbor table to map out active IP addresses and their corresponding hardware MAC addresses.

Unlike standard Windows tools, this script uses low-level Linux networking commands to provide real-time status updates on connected devices.

---

## 🚀 Installation & Setup

1. **Create the script file:**
Bash
   nano NetCheck.sh

    Apply execution permissions:
    Bash

    chmod +x NetCheck.sh

## 🛠️ Usage Instructions

Basic Execution:
Bash

./NetCheck.sh

Pro Tip (The "Wake-Up" Routine):

In Parrot OS, the neighbor table might be empty if the network is idle. If you get an "Empty Table" error, run a quick ping to refresh the cache before running the script:
Bash

ping -c 3 8.8.8.8
sudo ./NetCheck.sh

## 📊 Technical Details

    Command Core: Utilizes ip neigh show for modern Linux compatibility.

    Data Filtering: Employs awk for precise column alignment and grep for noise reduction.

    Visuals: Features a color-coded interface for easy reading in the Parrot terminal.

Status Meaning
REACHABLE Device is active and responding now.
STALE Device was active recently but is now idle.
DELAY/PROBE The system is currently checking if the device is still there.

## 📅 Development History

    v1.0.0: Initial concept tested in Git Bash.

    v1.1.0: Windows optimization.

    v1.2.0: Finalized for Parrot OS with Linux-native networking logic.

---

### How to use this

1. Open your terminal in Parrot.
2. Type `nano README.md`.
3. Paste the text above.
4. Press `Ctrl + O` then `Enter` to save, and `Ctrl + X` to exit.
