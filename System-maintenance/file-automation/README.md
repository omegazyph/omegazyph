# Downloads CleanBot

A lightweight Bash automation utility designed to keep your target Downloads directory clean and organized. It dynamically creates subdirectories based on file types and sorts files safely without overwriting existing data.

---

## Header Details

* **Script Name:** `Downloads_CleanBot.sh`
* **Author:** Omegazyph
* **Date Created:** 2026-01-04
* **Last Updated:** 2026-09-11
* **Target Directory:** `$HOME/Downloads`

---

## Core Features

* **Directory Safety Checks:** Verifies the existence of `$HOME/Downloads` before performing any operations, gracefully aborting if the target path is unavailable.

* **Automated Directory Generation:** Automatically detects and generates missing subdirectories (`Pictures`, `Documents`, `Music`, `Videos`, `Compressed`).

* **Safe Globbing (`shopt -s nullglob`):** Prevents wildcards from expanding into literal strings when specific file extensions are missing from the folder.

* **Overwrite Prevention (`mv -vn`):** Uses verbose and no-clobber flags during move operations, preserving existing files in target folders if a duplicate name is present.

* **Array-Based Counting:** Scans and counts matching file extensions prior to execution, providing exact item counts in terminal status messages.

* **Formatted ANSI Output:** Custom functions (`print_status`, `print_success`, `print_warning`, `print_error`) provide clean, color-coded visual feedback.

---

## Supported File Extensions

* **Pictures:** `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`
* **Documents:** `.pdf`, `.doc`, `.docx`, `.txt`, `.pages`, `.csv`
* **Music:** `.mp3`, `.wav`, `.m4a`, `.flac`
* **Videos:** `.mp4`, `.mov`, `.avi`, `.mkv`
* **Compressed:** `.zip`, `.tar`, `.gz`, `.rar`, `.7z`

---

## Directory Structure

system-maintenance/

└── file-automation/

    ├── Downloads_CleanBot.sh
    └── README.md

## Installation & Usage

1. **Make the script exutable:**

    chmod +x Downloads_CleanBot.sh

2. **Run the script:**

    ./Downloads_cleanBot.sh

## Configuration

* To modify the target location or add extra file types, adjust the configuration variables in the script:

TARGET_DIR="$HOME/Downloads"

TARGET_FOLDERS=("Pictures" "Documents" "Music" "Videos" "Compressed")
