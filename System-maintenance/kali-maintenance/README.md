# Kali Linux Automated System Maintenance

A robust Bash automation script built to execute end-to-end maintenance, software upgrades, database updates, network DNS checks, and system cleanup on Kali Linux environments.

---

## Header Details

* **Script Name:** `update_kali.sh`
* **Author:** Wayne Stock
* **Date Created:** 2024-01-21
* **Last Updated:** 2026-09-10
* **Target Environment:** Kali Linux / Debian-based systems

---

## Core Features

* **Privilege Guard:** Ensures execution under root (`$EUID -ne 0`) to prevent unauthorized or broken update runs.

* **Automated DNS Recovery:** Tests connectivity against `kali.org`. If DNS resolution fails, the script unsets the immutable attribute on `/etc/resolv.conf`, populates Cloudflare (`1.1.1.1`) and Google (`8.8.8.8`) primary/secondary nameservers, and locks the file with `chattr +i`.

* **Full System Upgrades:** Runs `apt-get update` followed by `apt-get dist-upgrade -y` to keep core packages up to date.

* **Kernel Meta-Package Upgrades:** Installs and updates `linux-headers-amd64` and `linux-image-amd64` using `--allow-change-held-packages`.

* **Security & Recon Tool Maintenance:**
  * Installs and refreshes `exploitdb`.
  * Triggers `searchsploit -u` guarded by a 60-second `timeout` to handle hanging connections safely.
  * Rebuilds Nmap Scripting Engine signatures with `nmap --script-updatedb`.

* **System Cleanup Routine:** Purges unused dependencies and flushes local archive caches using `apt-get autoremove --purge -y` and `apt-get clean`.

* **Interactive Reboot Prompt:** Checks `/var/run/reboot-required` and prompts for immediate system reboot via `/usr/sbin/reboot` if kernel changes were applied.

* **ANSI Color Output:** Custom output functions (`print_status`, `print_success`, `print_warning`, `print_error`) provide clean visual feedback in the terminal.

---

## Prerequisites

* **OS:** Kali Linux (or compatible Debian/Ubuntu distribution)

* **User Privileges:** Root access or elevated `sudo` rights

* **Required Binary Utilities:** `bash`, `ping`, `chattr`, `apt-get`, `timeout`, `searchsploit`, `nmap`

---

## File Structure

Project_Folder/

├── update_kali.sh

└── README.md

## Installation & Usage

chmod +x update_kali.sh
sudo ./update_kali.sh

## Coniguration & Notes

* DNS Fallback:

    Dynamic DNS Updates target 1.1.1.1 and 8.8.8.8.  if alternative local internal DNS servers are needed, update the sting inside the network & DNS Integrity Check section of update_kali.sh

* Searchsploit Exit Codes:

    The script accepts exit codes 0 and 1 from searchsploit -u to account for standard status returns during singature checks.
