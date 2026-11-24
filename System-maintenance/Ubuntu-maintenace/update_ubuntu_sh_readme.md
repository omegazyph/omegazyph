# update_Ubuntu.sh

An automated, color-coded maintenance script for Ubuntu servers that handles package repository updates, system and distribution upgrades, package/cache cleanup, root disk usage monitoring, and interactive reboot prompts.

## Features

- **Fail-Fast Execution:** Uses `set -e` at the global scope so the script stops immediately if any command returns a non-zero exit code.
- **4-Step Maintenance Workflow:**
  1. Updates APT package repositories (`sudo apt update`).
  2. Upgrades installed packages (`sudo apt upgrade -y`).
  3. Performs distribution and kernel/dependency upgrades (`sudo apt dist-upgrade -y`).
  4. Cleans up unused packages and caches (`autoremove`, `autoclean`, `clean`) and checks root (`/`) disk usage.
- **Disk Space Alerts:** Evaluates root partition usage (`df -P /`) and flags warnings at `>= 80%` and errors at `>= 90%`.
- **Standardized UI & Banners:** Uses dynamically centered ASCII banners and consistent status prefixes:
  - `[~]` — Status / active step (Magenta)
  - `[*]` — Info (Blue)
  - `[+]` — Success (Green)
  - `[!]` — Warning (Yellow)
  - `[X]` — Error (Red)
- **Reboot Detection:** Checks `/var/run/reboot-required` and prompts before rebooting (with a 5-second countdown if confirmed).
- **Direct Execution Guard:** Ensures `main "$@"` runs only when executed directly rather than sourced.

## Requirements

- Ubuntu / Debian-based system with `apt`, `awk`, and `df`
- `sudo` privileges for package management and optional reboot

## Usage

1. Make the script executable:

   ```bash
   chmod +x update_Ubuntu.sh
   ```

2. Run the script:

   ```bash
   ./update_Ubuntu.sh
   ```

## Author & Metadata

- **Script Name:** `update_Ubuntu.sh`
- **Author:** `omegazyph`
- **Created:** `2026-02-27`
- **Last Updated:** `2026-11-23`
