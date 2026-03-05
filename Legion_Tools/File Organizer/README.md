# 👻 File Ghost Organizer

## Script Metadata

* **Author:** omegazyph
* **Created:** 2026-01-07
* **Updated:** 2026-01-07
* **Environment:** Windows 11 Home (Lenovo Legion)
* **IDE:** VSCode

---

## 📝 Description

**File Ghost Organizer** is a Python-based automation utility designed to keep the Downloads folder clean and the Legion C: drive optimized. It scans your user Downloads directory and teleports files into specific, categorized subfolders based on their extensions.

## ⚡ Features

* **Hacker UI:** Custom `print_hacker` function for a scrolling terminal aesthetic with green ANSI color coding.
* **C: Drive Optimization:** Keeps system drives lean by preventing "Download clutter."
* **Smart Sorting:** Automatically detects and moves the following categories:
  * **Scripts:** `.py`, `.sh`, `.bat`, `.ps1`
    * **Documents:** `.pdf`, `.docx`, `.txt`, `.xlsx`
    * **Media:** `.jpg`, `.png`, `.mp4`, `.mp3`
    * **Installers:** `.exe`, `.msi`
    * **Archives:** `.zip`, `.rar`, `.7z`

## 🚀 Setup & Usage

### Running in VSCode

1. Open the folder containing `file_ghost_organizer.py` in **VSCode**.
2. Ensure your terminal is open.
3. Run the script:

bash
    python file_ghost_organizer.py

### Running via Bash

Since you enjoy using Bash, you can also execute this from your terminal:

bash
bash -c "python file_ghost_organizer.py"

## 🛠️ Technical Details

The script uses standard Python libraries, so no external pip installs are required:

    os: To handle file paths and directory creation.

    shutil: To move files across the filesystem.

    time: To control the "hacker-style" text speed.
