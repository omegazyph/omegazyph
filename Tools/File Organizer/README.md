# 👻 File Ghost Organizer

## Script Metadata

* **Author:** omegazyph
* **Created:** 2026-01-07
* **Updated:** 2026-11-21
* **Environment:** Windows 11 Home (Lenovo Legion) / Linux
* **IDE:** VSCode

---

## 📝 Description

**File Ghost Organizer** is a Python-based automation utility designed to keep the `Downloads` folder clean and the Legion `C:` drive optimized. It scans your user `Downloads` directory and sorts files into categorized subfolders based on extension rules defined in an external `destinations.json` configuration file.

## 📂 Project Structure

```text
Python_Utilities/
  └── scripts/
        ├── destinations.json
        ├── file_ghost_organizer.py
        └── README.md
```

## ⚡ Features

* **Unified ANSI Terminal UI:** Uses `print_hacker` typewriter output, dynamically centered ASCII banners (`print_ascii_banner` / `print_ascii_ending`), and color-coded status messages (`print_message`).
* **External JSON Configuration:** Loads category-to-extension mappings from `destinations.json` so you can add new folders or file extensions without editing the Python script.
* **C: Drive Optimization:** Keeps system drives lean by preventing download clutter.
* **Resilient Error Handling:** Catches `OSError` and `json.JSONDecodeError` issues during configuration loading and file moves so locked or inaccessible files are reported cleanly without crashing the run.
* **Default Sorting Categories:**
  * **Scripts:** `.py`, `.sh`, `.bat`, `.ps1`
  * **Documents:** `.pdf`, `.docx`, `.txt`, `.xlsx`, `.ods`
  * **Media:** `.jpg`, `.png`, `.mp4`, `.mp3`
  * **Installers:** `.exe`, `.msi`
  * **Archives:** `.zip`, `.rar`, `.7z`

## 🚀 Setup & Usage

### Running in VSCode

1. Open the folder containing `file_ghost_organizer.py` and `destinations.json` in **VSCode**.
2. Open the integrated terminal.
3. Run the script:

```bash
python file_ghost_organizer.py
```

### Running via Bash

You can also execute the script directly from a Bash shell:

```bash
bash -c "python file_ghost_organizer.py"
```

## 🛠️ Technical Details

The script relies strictly on Python's built-in standard library, so no external `pip` packages are required:

* `json`: Loads and parses folder/extension rules from `destinations.json`.
* `os`: Resolves paths, clears the terminal screen, lists files, and creates category directories.
* `shutil`: Moves matched files into their destination subfolders.
* `sys`: Flushes standard output buffers for live character-by-character printing.
* `time`: Controls the typewriter animation speed and scan pauses.
  