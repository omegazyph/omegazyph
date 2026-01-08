# LEGION PRIME v1.0

## Project Header

- **Date:** 2026-01-07
- **Author:** omegazyph
- **Updated:** 2026-01-07
- **Description:** A specialized "God-Mode" suite designed for Windows 11 Home (Lenovo Legion).

---

## 🚀 Features

The **LegionTools** class provides a centralized command center for:

    * **System Optimization:** Cleans DNS cache and triggers SSD Trim for peak performance.
    * **Hardware Diagnostics:** Real-time monitoring of RAM, Battery health, and C: Drive capacity.
    * **Global Intelligence:** Fetches local weather via `wttr.in` and top tech news from Hacker News.
    * **Network Probing:** Integrated speed test to verify upload/download stability.

## 🛠️ Requirements

This suite requires **Python 3.x** and the following libraries:

- `psutil` (System and hardware monitoring)
- `requests` (API data retrieval)
- `speedtest-cli` (Network testing)

## 📂 Installation & Setup

1. Clone or move all files into the `Legion-Prime-Core` folder.
2. Install dependencies via terminal:
bash
   pip install psutil requests speedtest-cli

    Run the launch_legion.bat file as Administrator to ensure the Optimizer functions (SSD Trim) have the necessary permissions.

## 📄 File Structure

    legion_prime.py: The main Python logic and LegionTools class.

    launch_legion.bat: Windows Batch launcher for quick execution.

    README.md: Project documentation and setup guide.

Developed for the Legion high-performance environment.

---

### Folder Organization Tip

In your VS Code workspace, your folder should now look like this:

## 📁 **Legion-Prime-Core**

    * 📄 `legion_prime.py`
    * 📄 `launch_legion.bat`
    * 📄 `README.md`
