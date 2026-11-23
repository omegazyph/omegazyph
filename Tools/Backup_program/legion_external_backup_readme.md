# 🛡️ Legion-External-Backup (`legion_to_external_backup.py`)

A custom Python-based incremental backup utility designed for the **Lenovo Legion (Windows 11 Home)** environment. It reads project paths and exclusions from `backup_config.json` and synchronizes new or updated files to your external backup drive (`Z:\`) with a styled ANSI terminal interface.

---

## 🚀 Overview

* **Incremental Sync:** Compares modification timestamps (`mtime`) via `os.walk` and copies files with `shutil.copy2` only when they are missing or newer at the destination.
* **External Configuration:** All target drives, source/destination pairs, and excluded directories are managed inside `backup_config.json` without modifying the Python script.
* **Directory Pruning:** Skips excluded folders (such as `.git` and `private`) in-place during directory traversal.
* **Terminal UI:** Uses standardized ANSI color-coded status markers (`[+]`, `[*]`, `[!]`, `[X]`) and centered ASCII banners.

---

## 📂 Project Structure

```text
Legion-External-Backup/
  ├── README.md
  ├── launch_backup.bat
  ├── backup_config.json
  └── legion_to_external_backup.py
```

---

## 🛠️ Setup & Configuration

### 1. Requirements

* **OS:** Windows 11
* **Python:** Python 3.10+ (uses standard library modules only: `json`, `os`, `shutil`, `sys`, `time`)
* **Terminal:** Best experienced in Windows Terminal with ANSI color support enabled.

### 2. Configure `backup_config.json`

Place `backup_config.json` in the same directory as `legion_to_external_backup.py` and define your target drive, exclusions, and backup tasks:

```json
{
  "target_drive": "Z:\\",
  "excluded_dirs": [
    ".git",
    "private"
  ],
  "backup_tasks": [
    {
      "name": "omegazyph",
      "source": "C:\\Users\\omega\\Desktop\\omegazyph",
      "destination": "Z:\\Windows\\Documents\\Git hub projects\\omegazyph_back_up"
    },
    {
      "name": "Freelance-Portfolio-Project",
      "source": "C:\\Users\\omega\\Desktop\\Freelance-Portfolio-Project",
      "destination": "Z:\\Windows\\Documents\\Git hub projects\\Freelance-Portfolio-Project_Back_up"
    }
  ]
}
```

---

## 🖥️ Usage

Ensure your external target drive (`Z:\`) is connected, then run the script directly or via the batch launcher:

### Option 1: Batch Launcher (Recommended)

Double-click `launch_backup.bat` or run it from the command prompt:

```bat
launch_backup.bat
```

### Option 2: Direct Python Execution

```bash
python legion_to_external_backup.py
```

Press `Ctrl + C` at any time to terminate the protocol cleanly.

---

## 📜 Credits & Metadata

* **Script:** `legion_to_external_backup.py`
* **Author:** omegazyph
* **Last Updated:** 2026-11-23
* **Hardware:** Lenovo Legion (Windows 11 Home)
