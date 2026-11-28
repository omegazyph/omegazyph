# Smart Backup Utility (`smart_backup.py`)

A lightweight, incremental Python backup utility optimized for VS Code that copies only new or modified files from a `my_files` directory into a `backup_folder` directory relative to the script's location, complete with ANSI terminal styling and a typewriter-style console output.

## Features

* **Incremental Timestamp Comparison:** Compares last-modified timestamps (`os.path.getmtime()`) between source and destination files so unchanged files are skipped rather than recopied.
* **Path-Agnostic Execution:** Uses `os.path.dirname(os.path.abspath(__file__))` and `os.path.join()` to locate `my_files` and `backup_folder` relative to the script regardless of your workspace's current working directory.
* **Safe Folder Initialization:** Automatically creates `backup_folder` if missing and catches `OSError` to exit cleanly if directory creation fails.
* **Resilient File Copying:** Uses `shutil.copy2()` to preserve file metadata and wraps each file check and copy in an `OSError` handler so a single locked or unreadable file does not halt the rest of the backup.
* **Unified Terminal UI & Summary:** Features a custom ASCII startup logo (`OMEGAZYPH_LOGO`), centered banners, ANSI color constants, categorized status messages (`error`, `info`, `status`, `success`, and `warning`), and a summary breakdown of updated, skipped, and failed files.

## Project Structure

```text
.
├── smart_backup.py
├── README.md
├── my_files/        # Source directory containing files to back up
└── backup_folder/   # Destination directory created automatically if missing
```

## Requirements

* **Python 3.x** (uses only Python standard library modules: `os`, `shutil`, `sys`, and `time`)
* A terminal or console that supports ANSI escape sequences for full color rendering

## Usage

1. Place `smart_backup.py` in your target working directory.
2. Create a `my_files` folder in the same directory as `smart_backup.py` and add the files you want to back up.
3. Run the script from your terminal or VS Code:

```bash
python smart_backup.py
```

Or make it executable on Unix-like systems and run it directly:

```bash
chmod +x smart_backup.py
./smart_backup.py
```

## Behavior & Edge Cases

* **Missing `my_files` Folder:** Logs an error message and exits `main()` cleanly before attempting to create `backup_folder`.
* **Backup Folder Creation Failure:** Catches `OSError` on `os.makedirs()`, logs the error details, and exits early.
* **Unchanged Files:** If a file already exists in `backup_folder` with a modification timestamp greater than or equal to the source file, it is skipped and counted toward `Files Skipped`.
* **Subdirectories:** Checks `os.path.isfile(source_path)` before processing so nested directories inside `my_files` are ignored.
* **Copy or Metadata Errors:** Catches `OSError` per file, logs the failure, increments `Files Failed`, and continues processing remaining files before printing the summary and completion banner.

## Author

* **Author:** omegazyph
* **Created:** 2026-01-05
* **Updated:** 2026-11-27
