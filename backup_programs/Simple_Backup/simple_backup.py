#!/usr/bin/env python

# ======================================================================
# Date:         2026-01-05
# Script Name:  simple_backup.py
# Author:       omegazyph
# Updated:      2026-11-27
# Description:  This program automatically finds its own location and
#               copies files from a 'my_files' folder to a 'backup_folder'.
# ======================================================================

# region --- Imports ---
# Import operating system helpers for path handling and clearing the terminal screen
import os

# Import high-level file utilities for copying files while preserving metadata
import shutil

# Import standard output controls for live character-by-character terminal output
import sys

# Import time utilities for delays during the typewriter effect
import time

# endregion

# region --- ANSI Color Codes ---
# Define bold ANSI escape sequences for colored terminal output
BLUE = "\033[1;34m"
BOLD = "\033[1m"
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
MAGENTA = "\033[38;2;255;0;144m"
PURPLE = "\033[1;35m"
RED = "\033[1;31m"
RESET = "\033[0m"
YELLOW = "\033[1;33m"
# endregion

# region --- Logo & UI Functions ---
# Store the custom ASCII startup logo as a raw multi-line string
OMEGAZYPH_LOGO = r"""
   ___  __  __ _____ ____    _   ______     ______  _   _
  / _ \|  \/  | ____/ ___|  / \  |__  /\ \ / /  _ \| | | |
 | | | | |\/| |  _|| |  _  / _ \   / /  \ V /| |_) | |_| |
 | |_| | |  | | |__| |_| |/ ___ \ / /_   | | |  __/|  _  |
  \___/|_|  |_|_____\____/_/   \_/____|  |_| |_|   |_| |_|
                        OMEGAZYPH
"""


def print_logo(logo_text=OMEGAZYPH_LOGO, color=PURPLE):
    """Print the startup logo using the typewriter effect and color formatting."""
    # Iterate line by line so multi-line ASCII art renders with proper spacing
    for line in logo_text.splitlines():
        if line:
            print_color(f"{BOLD}{color}{line}{RESET}")
        else:
            pass


def print_color(text, color=CYAN):
    """Print text one character at a time with a short delay for a typewriter effect."""
    # Apply the chosen ANSI color before writing characters to standard output
    sys.stdout.write(color)
    # Write each character and flush standard output immediately so delays appear live
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.01)
    # Reset terminal formatting and end the current line
    print(RESET)


def print_ascii_banner(banner_title="Default Title Starting"):
    """Print a dynamically centered ASCII banner with top and bottom borders."""
    # Define the total character width for the banner border
    total_width = 65
    # Calculate leading spaces needed to center the title inside the banner
    title_length = len(banner_title)
    padding = (total_width - title_length) // 2

    # Build the padding spaces and horizontal border line
    spaces = " " * padding
    separator_line = "=" * total_width

    # Print the top border, centered title, and bottom border
    print_color(f"{PURPLE}{separator_line}{RESET}")
    print_color(f"{BOLD}{BLUE}{spaces}{banner_title}{RESET}")
    print_color(f"{PURPLE}{separator_line}{RESET}")


def print_message(message_type, message_text=""):
    """Print formatted status messages using category prefixes and ANSI colors."""
    # Select the matching prefix symbol and ANSI color for the message type
    if message_type == "error":
        print_color(f"{BOLD}{RED}[X] {message_text}{RESET}")
    elif message_type == "info":
        print_color(f"{BOLD}{BLUE}[*] {message_text}{RESET}")
    elif message_type == "status":
        print_color(f"{BOLD}{MAGENTA}[~] {message_text}{RESET}")
    elif message_type == "success":
        print_color(f"{BOLD}{GREEN}[+] {message_text}{RESET}")
    elif message_type == "warning":
        print_color(f"{BOLD}{YELLOW}[!] {message_text}{RESET}")
    else:
        # Print plain text when no known message category is specified
        print(message_text)

# endregion

# region --- Functions ---
def run_backup():
    """Copy regular files from 'my_files' into 'backup_folder' next to this script."""
    # Resolve the directory containing this script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Build full paths for the source and destination folders
    source_folder = os.path.join(script_directory, "my_files")
    backup_folder = os.path.join(script_directory, "backup_folder")

    # Stop early if the source folder does not exist
    if not os.path.exists(source_folder):
        print_message("error", f"Error: Could not find '{source_folder}'")
        print_message("warning", "Please make sure the folder is named correctly.")
        return

    # Create the destination backup folder if it does not already exist
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
        print_message("info", f"Creating backup directory at: {backup_folder}")

    # Retrieve entries inside the source folder and check if it is empty
    files = os.listdir(source_folder)

    if not files:
        print_message("warning", "The source folder is empty.")
        return

    # Copy each regular file while handling any operating system copy errors
    for file_name in files:
        source_path = os.path.join(source_folder, file_name)
        destination_path = os.path.join(backup_folder, file_name)

        if os.path.isfile(source_path):
            try:
                shutil.copy2(source_path, destination_path)
                print_message("success", f"Backed up: {file_name}")
            except OSError as error:
                print_message("error", f"Failed to back up '{file_name}': {error}")

# endregion

# region --- Main Process ---
def main():
    """Clear the screen, display startup and completion banners, and run the backup."""
    # Clear the terminal screen across Windows and Unix-like shells
    os.system("cls" if os.name == "nt" else "clear")

    # Display the startup logo and banner
    print_logo()
    print_ascii_banner("Starting Backup Process")

    # Execute the file backup routine
    run_backup()

    # Display the completion banner
    print_ascii_banner("Backup Complete")


# endregion

if __name__ == "__main__":
    main()