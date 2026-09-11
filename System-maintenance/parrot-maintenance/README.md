# Parrot Security OS Automated System Maintenance

A comprehensive Bash automation script designed to manage system updates, upgrades, kernel dependency synchronization, security tool database maintenance, DNS health verification, and overall cleanup on Parrot Security OS environments.

---

## Header Details

* **Script Name:** `update_parrot.sh`
* **Author:** Wayne Stock
* **Date Created:** 2026-09-10
* **Last Updated:** 2026-09-10
* **Target Environment:** Parrot Security OS / Debian-based systems

---

## Core Features

* **Privilege Enforcement:** Verifies execution under root (`$EUID -ne 0`) before running administrative operations.

* **Automated DNS Recovery:** Tests reachability against `parrotsec.org`. If DNS resolution fails, the script unlocks `/etc/resolv.conf`, populates Cloudflare (`1.1.1.1`) and Google (`8.8.8.8`) primary and secondary nameservers, and applies the immutable file attribute (`chattr +i`).

* **Package Synchronization & Upgrades:** Executes `apt-get update` and `apt-get dist-upgrade -y` to upgrade system packages and base distribution builds.

* **Dynamic Kernel Headers Update:** Automatically detects the running kernel version using `linux-headers-$(uname -r)` and updates held kernel dependencies using `--allow-change-held-packages`.

* **Penetration Testing Database Maintenance:**
  * Installs and refreshes `exploitdb`.
  * Runs `searchsploit -u` guarded by a 60-second `timeout` execution window.
  * Rebuilds Nmap Scripting Engine signatures via `nmap --script-updatedb`.

* **System Cleanup:** Purges unneeded dependencies and flushes local installer archives using `apt-get autoremove --purge -y` and `apt-get clean`.

* **Reboot Detection:** Monitors `/var/run/reboot-required` and prompts for an optional immediate system restart via `/usr/sbin/reboot`.

* **ANSI Color Output:** Formatted terminal logging functions (`print_status`, `print_success`, `print_warning`, `print_error`) provide clear visual tracking during execution.

---

## Prerequisites

* **OS:** Parrot Security OS (or compatible Debian/Ubuntu distribution)
* **User Privileges:** Root user access or elevated `sudo` permissions
* **Required Utilities:** `bash`, `ping`, `chattr`, `apt-get`, `uname`, `timeout`, `searchsploit`, `nmap`

---

## Directory Structure

system-maintenance/

└── parrot-maintenance/

    ├── update_parrot.sh
    └── README.md
---

## Installation & Usage

chmod +x update_parrot.sh
sudo ./update_parrot.sh

---

## Configuration & Notes

* Kernel Dynamic Matching:

    Unlike generic updates, this script dynamically targets linux-headers-$(uname -r) to match your active kernel release on Parrot Security OS.

* DNS Override:

    Fallback nameservers default to Cloudflare (1.1.1.1) and Google (8.8.8.8). Edit the Network & DNS Integrity Check section inside update_parrot.sh to adjust fallback IP addresses if needed
