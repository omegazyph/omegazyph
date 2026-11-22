# Legion Optimizer (`legion_optimizer.py`)

A cross-platform command-line diagnostic and system maintenance utility for Windows and Linux workstations. It verifies elevated privileges, checks battery health via `psutil`, and runs platform-appropriate drive TRIM, DNS cache flush, and temporary file cleanup tasks with structured terminal feedback.

## Project Structure

``` python
Python_Utilities/
├── requirements.txt
├── README_2.md
└── scripts/
    └── legion_optimizer.py

```

## Features

* **Automatic Privilege Elevation (`ensure_elevated`)**

  * **Windows:** Checks `IsUserAnAdmin()` and relaunches the script through Windows UAC (`ShellExecuteW` with `"runas"`).

  * **Linux / POSIX:** Verifies `os.geteuid() == 0` and re-executes the script via `sudo` if not already running as root.

* **Stable Battery Diagnostics (`get_battery_info`)**

  * Queries `psutil.sensors_battery()` to display current charge percentage and AC power status (`Plugged In` or `On Battery`), or logs a warning if no battery sensor is present.

* **Cross-Platform Drive TRIM**

  * **Windows:** Runs `defrag C: /O`.

  * **Linux:** Checks for `fstrim` and executes `fstrim -v /`. Gracefully skips with a non-fatal warning on virtual machines, live USBs, or filesystems that do not support discard operations.

* **Cross-Platform DNS Cache Flush**

  * **Windows:** Executes `ipconfig /flushdns`.

  * **Linux:** Checks for `resolvectl` and runs `resolvectl flush-caches`, skipping cleanly with a warning on distributions (such as Kali) that do not use `systemd-resolved` by default.

* **Temporary File Cleanup**

  * **Windows:** Purges temporary files from `%TEMP%`.

  * **Linux:** Cleans temporary contents inside `/tmp` while preserving the `/tmp` directory itself.

* **Styled Terminal UI**

  * Includes dynamically centered ASCII startup and closing banners, typewriter text output (`print_hacker`), and standardized color-coded status markers (`[+]`, `[*]`, `[!]`, `[X]`).

## Requirements

* **Python:** 3.8 or higher

* **Third-Party Packages:** `psutil` (listed in `requirements.txt`)

* **Permissions:** Administrator privileges on Windows or `sudo` / `root` access on Linux

## Installation

1. Navigate to the project root directory:

   ```bash
   cd Python_Utilities
   
   ```

2. Install the required dependency:

   ``` bash
   pip install -r requirements.txt
   
   ```

## Usage

### Windows

Run from Command Prompt, PowerShell, or double-click the script. If not already elevated, a Windows UAC prompt will request Administrator approval:

```bash
python scripts\legion_optimizer.py

```

### Linux (Debian / Ubuntu / Kali)

Run directly with Python; if you are not `root`, the script will invoke `sudo` automatically:

```bash
python3 scripts/legion_optimizer.py

```

## Notes for Virtual Machines & Kali Linux

* **TRIM in VMs / Live Environments:** Virtual disks and overlay filesystems often do not pass discard commands to host storage. When `fstrim` reports `the discard operation is not supported`, the script logs a `[!]` warning and continues without failing.

* **DNS Management on Kali:** Because Kali does not enable `systemd-resolved` by default, `resolvectl` may not be installed. The script detects this via `shutil.which("resolvectl")` and skips the DNS flush cleanly.
