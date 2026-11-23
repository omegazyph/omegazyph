# LEGION PRIME v1.1

## Project Header

- **Date:** 2026-01-07
- **Author:** omegazyph
- **Updated:** 2026-11-23
- **Description:** A specialized command-line diagnostic, briefing, and system maintenance utility designed for Windows 11 Home (Lenovo Legion), with cross-platform guardrails for non-Windows environments.

---

## Features

The diagnostic and maintenance suite provides a centralized command center for:

- **System Optimization:** Runs SSD optimization (`defrag C: /O`) and DNS cache flush (`ipconfig /flushdns`) on Windows when elevated, and reports RAM utilization.
- **Hardware Diagnostics:** Checks battery charge/charging status and free storage space (`C:\` on Windows, `/` on POSIX systems) using `psutil`.
- **Global Intelligence:** Fetches current weather via `wttr.in` and the top 3 stories from Hacker News.
- **Network Probing:** Runs server selection, download speed, upload speed, and ping checks using `speedtest-cli`.

---

## Requirements

This suite requires **Python 3.x** and the following libraries:

- `psutil` (System and hardware monitoring)
- `requests` (API data retrieval)
- `speedtest-cli` (Network testing)

---

## Installation & Setup

1. Place all project files inside the `Legion-Prime-Core` folder.
2. Install dependencies via terminal:

   ```bash
   pip install psutil requests speedtest-cli
   ```

3. Run `launch_legion.bat` so the script can request Administrator privileges, locate Python, execute `legion_prime.py`, and pause before closing.

---

## File Structure

- `legion_prime.py`: Main Python diagnostic, briefing, and maintenance script.
- `launch_legion.bat`: Windows Batch launcher that checks/requests Administrator privileges, locates Python, runs `legion_prime.py`, and keeps the window open.
- `README.md`: Project documentation and setup guide.

Developed for the Legion high-performance environment.

---

### Folder Organization

In your VS Code workspace, your folder should look like this:

```text
Legion-Prime-Core/
├── README.md
├── launch_legion.bat
└── legion_prime.py
```
