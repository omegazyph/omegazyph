# Simple Backup Utility (`simple_backup.py`)

A lightweight, self-locating Python backup utility that copies regular files from a `my_files` directory into a `backup_folder` directory relative to the script's location, complete with ANSI terminal styling and a typewriter-style console output.

## Features

- **Path-Agnostic Execution:** Uses `os.path.abspath(__file__)` and `os.path.join()` to locate `my_files` and `backup_folder` relative to the script regardless of your current working directory.
- **Automatic Directory Setup:** Creates `backup_folder` automatically if it does not already exist.
- **Resilient File Copying:** Uses `shutil.copy2()` to preserve file metadata and wraps each copy operation in an `OSError` handler so a single locked or unreadable file does not halt the rest of the backup.
- **Unified Terminal UI:** Features a custom ASCII startup logo (`OMEGAZYPH_LOGO`), centered banners, ANSI color constants, and categorized status messages (`error`, `info`, `status`, `success`, and `warning`).

## Project Structure

```text
.
├── simple_backup.py
├── README.md
├── my_files/        # Source directory containing files to back up
└── backup_folder/   # Destination directory created automatically if missing
```

## Requirements

- **Python 3.x** (uses only Python standard library modules: `os`, `shutil`, `sys`, and `time`)
- A terminal or console that supports ANSI escape sequences for full color rendering

## Usage

1. Place `simple_backup.py` in your target working directory.
2. Create a `my_files` folder in the same directory as `simple_backup.py` and add the files you want to back up.
3. Run the script from your terminal or editor:

```bash
python simple_backup.py
```

Or make it executable on Unix-like systems and run it directly:

```bash
chmod +x simple_backup.py
./simple_backup.py
```

## Behavior & Edge Cases

- **Missing `my_files` Folder:** Logs an error and warning message, then exits `run_backup()` cleanly without creating a backup folder.
- **Empty `my_files` Folder:** Logs a warning message and returns early without copying anything.
- **Subdirectories:** Checks `os.path.isfile(source_path)` before copying so nested folders are skipped rather than passed to `shutil.copy2()`.
- **Copy Failures:** Catches `OSError` per file, prints an error message with details, and continues processing remaining files before displaying the completion banner.

## Author

- **Author:** omegazyph
- **Created:** 2026-01-05
- **Updated:** 2026-11-27