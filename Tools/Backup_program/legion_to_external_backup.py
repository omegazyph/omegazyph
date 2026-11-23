#!/usr/bin/env python

# ===============================================================================
# Project Folder Structure:
#   Legion-External-Backup/
#     ├── README.md
#     ├── launch_backup.bat
#     ├── backup_config.json
#     └── legion_to_external_backup.py
#
# Date:         2026-01-07
# Script Name:  legion_to_external_backup.py
# Author:       omegazyph
# Updated:      2026-11-23
# Description:  Synchronizes configured project directories from backup_config.json
#               to the external drive using timestamp comparison, directory pruning,
#               and a hacker-style status UI.
# ===============================================================================


# region --- Imports ---
# Import json for loading external backup task definitions from backup_config.json
import json

# Import os for filesystem paths, directory walking, and screen clearing
import os

# Import shutil for copying files while preserving metadata via copy2
import shutil

# Import sys for direct output flushing and clean exit handling
import sys

# Import time for character pacing in the terminal UI
import time

# endregion


# region --- ANSI Color Codes ---
# Define bold ANSI escape sequences for colored terminal output
BLUE = "\033[1;34m"
BOLD = "\033[1m"
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
PURPLE = "\033[1;35m"
RED = "\033[1;31m"
RESET = "\033[0m"
YELLOW = "\033[1;33m"
# endregion


# region --- UI Functions ---
def print_color(text, color=CYAN):
    """Print text one character at a time with a short delay for a typing effect."""
    # Apply the selected ANSI color before writing characters
    sys.stdout.write(color)
    # Write each character and flush standard output immediately so delays appear live
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.01)
    # Reset text attributes and end the line
    print(RESET)


def print_ascii_banner(banner_title="Default Title"):
    """Print a dynamically centered ASCII banner frame for section or closing titles."""
    # Set the total character width for the banner border
    total_width = 65
    # Calculate leading spaces needed to center the title inside the banner width
    title_length = len(banner_title)
    padding = max(0, (total_width - title_length) // 2)

    # Generate the exact number of leading spaces for centering
    spaces = " " * padding

    # Build the horizontal border line
    separator_line = "=" * total_width

    # Print the top border, centered title, and bottom border using the typing effect
    print_color(f"{PURPLE}{separator_line}{RESET}")
    print_color(f"{BOLD}{BLUE}{spaces}{banner_title}{RESET}")
    print_color(f"{PURPLE}{separator_line}{RESET}")


def print_message(message_type, message_text=""):
    """Print status messages using standardized prefixes and ANSI colors."""
    # Choose the prefix marker and ANSI color based on the message type
    if message_type == "error":
        print_color(f"{BOLD}{RED}[X] {message_text}{RESET}")
    elif message_type == "info":
        print_color(f"{BOLD}{BLUE}[*] {message_text}{RESET}")
    elif message_type == "status":
        print_color(f"{BOLD}{CYAN}[*] {message_text}{RESET}")
    elif message_type == "success":
        print_color(f"{BOLD}{GREEN}[+] {message_text}{RESET}")
    elif message_type == "warning":
        print_color(f"{BOLD}{YELLOW}[!] {message_text}{RESET}")
    else:
        # Print plain text when the message type does not match a known category
        print(message_text)
# endregion


# region --- Configuration Loader ---
def get_default_config_path():
    """Resolve backup_config.json next to this script file."""
    script_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_directory, "backup_config.json")


def load_backup_config(config_path=None):
    """
    Load and validate backup configuration from a JSON file.

    Returns a tuple of (target_drive, excluded_dirs, backup_tasks) or None on failure.
    """
    resolved_path = config_path if config_path else get_default_config_path()

    if not os.path.exists(resolved_path):
        print_message("error", f"Configuration file not found: {resolved_path}")
        return None

    try:
        with open(resolved_path, "r", encoding="utf-8") as config_file:
            config_data = json.load(config_file)
    except (OSError, json.JSONDecodeError) as load_error:
        print_message("error", f"Failed to read configuration '{resolved_path}': {load_error}")
        return None

    if not isinstance(config_data, dict):
        print_message("error", "Configuration root must be a JSON object.")
        return None

    target_drive = config_data.get("target_drive", "Z:\\")
    raw_tasks = config_data.get("backup_tasks", [])
    raw_excluded = config_data.get("excluded_dirs", [".git", "private"])

    if not isinstance(target_drive, str) or not target_drive.strip():
        print_message("error", "Invalid 'target_drive' value in backup_config.json.")
        return None

    if not isinstance(raw_tasks, list) or len(raw_tasks) == 0:
        print_message("error", "No 'backup_tasks' entries found in backup_config.json.")
        return None

    excluded_dirs = set()
    if isinstance(raw_excluded, list):
        for entry in raw_excluded:
            if isinstance(entry, str) and entry.strip():
                excluded_dirs.add(entry.strip())

    validated_tasks = []
    for index, task in enumerate(raw_tasks, start=1):
        if not isinstance(task, dict):
            print_message("warning", f"Skipping task #{index}: entry is not an object.")
            continue

        source_path = task.get("source", "")
        destination_path = task.get("destination", "")
        task_name = task.get("name", "")

        if not isinstance(source_path, str) or not source_path.strip():
            print_message("warning", f"Skipping task #{index}: missing 'source' path.")
            continue

        if not isinstance(destination_path, str) or not destination_path.strip():
            print_message("warning", f"Skipping task #{index}: missing 'destination' path.")
            continue

        if not isinstance(task_name, str) or not task_name.strip():
            task_name = os.path.basename(os.path.normpath(source_path))

        validated_tasks.append({
            "name": task_name.strip(),
            "source": source_path.strip(),
            "destination": destination_path.strip(),
        })

    if not validated_tasks:
        print_message("error", "No valid backup tasks remained after validation.")
        return None

    return target_drive.strip(), excluded_dirs, validated_tasks
# endregion


# region --- Backup Engine ---
def sync_folders(source, destination, excluded_dirs):
    """
    Synchronize files from source to destination when missing or newer.

    Excludes directories listed in excluded_dirs from traversal and returns a tuple
    of (updated_count, skipped_count, had_errors).
    """
    updated_count = 0
    skipped_count = 0
    had_errors = False

    if not os.path.exists(source):
        print_message("error", f"Source '{source}' missing. Skipping...")
        return 0, 0, True

    try:
        os.makedirs(destination, exist_ok=True)
    except OSError as mkdir_error:
        print_message("error", f"Cannot create destination '{destination}': {mkdir_error}")
        return 0, 0, True

    for current_root, directories, files in os.walk(source):
        # Prune excluded directories in-place so os.walk does not descend into them
        directories[:] = [
            directory_name
            for directory_name in directories
            if directory_name not in excluded_dirs
        ]

        relative_path = os.path.relpath(current_root, source)
        dest_dir = destination if relative_path == "." else os.path.join(destination, relative_path)

        try:
            os.makedirs(dest_dir, exist_ok=True)
        except OSError as dir_error:
            print_message("error", f"Error creating folder {dest_dir}: {dir_error}")
            had_errors = True
            continue

        for filename in files:
            source_file = os.path.join(current_root, filename)
            destination_file = os.path.join(dest_dir, filename)

            try:
                should_copy = False
                if (
                    not os.path.exists(destination_file)
                    or os.path.getmtime(source_file) > os.path.getmtime(destination_file)
                    ):
                    should_copy = True

                if should_copy:
                    shutil.copy2(source_file, destination_file)
                    updated_count += 1
                    print_message("success", f"Moved file: {filename}")
                else:
                    skipped_count += 1
            except OSError as copy_error:
                print_message("error", f"Error copying {filename}: {copy_error}")
                had_errors = True

    return updated_count, skipped_count, had_errors


def run_backup_protocol():
    """Load backup_config.json, verify target drive availability, and run syncs."""
    os.system("cls" if os.name == "nt" else "clear")

    print_ascii_banner("OMEGAZYPH MULTI-SYNC PROTOCOL: LACIE_Z_DRIVE")

    loaded_config = load_backup_config()
    if loaded_config is None:
        print_ascii_banner("BACKUP CONFIGURATION ERROR")
        return

    target_drive, excluded_dirs, backup_tasks = loaded_config

    # Verify the external backup target drive is mounted before syncing
    if not os.path.exists(target_drive):
        print_message("error", f"Target drive '{target_drive}' not found.")
        print_ascii_banner("BACKUP TARGET MISSING")
        return

    total_updated = 0
    total_skipped = 0
    tasks_with_errors = 0

    for task in backup_tasks:
        task_name = task["name"]
        source_path = task["source"]
        destination_path = task["destination"]

        print_message("info", f"\nSTARTING SYNC: {task_name} -> {target_drive}")
        updated_files, skipped_files, task_had_error = sync_folders(
            source_path,
            destination_path,
            excluded_dirs,
        )
        if task_had_error:
            tasks_with_errors += 1
        total_updated += updated_files
        total_skipped += skipped_files

    # Print summary statistics for the run
    print_color("\n" + "=" * 40)
    print_color(f"  Total Files Updated: {total_updated}")
    print_color(f"  Total Files Skipped: {total_skipped}")
    print_color("=" * 40)

    if tasks_with_errors == 0:
        print_ascii_banner("ALL BACKUPS SUCCESSFUL")
    else:
        print_ascii_banner("BACKUPS COMPLETED WITH WARNINGS")
# endregion


# region --- main Process ---
def main():
    """Entry point with clean Ctrl+C handling."""
    try:
        run_backup_protocol()
    except KeyboardInterrupt:
        print_message("error", "\nProtocol Terminated.")
        sys.exit(0)
# endregion


if __name__ == "__main__":
    main()
