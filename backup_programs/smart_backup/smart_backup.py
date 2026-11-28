#!/usr/bin/env python

# =====================================================================================
# Date:         2026-01-05
# Script Name:  smart_backup.py
# Author:       omegazyph
# Updated:      2026-11-27
# Description:  An incremental backup script optimized for VS Code. 
#               Copies new/modified files from 'my_files' to 'backup_folder'.
# =====================================================================================

# region --- Imports ---

# Import operating system interface helpers for clearing the terminal screen
import os

# Import high-level file and folder operations for copying files while preserving metadata
import shutil

# Import standard output and flush controls for character-by-character output
import sys

# Import time utilities for character delays during typewriter printing
import time

# endregion

# region --- ANSI Color Codes ---
# Define bold ANSI escape sequences for colored terminal output
BLUE = "\033[1;34m"
BOLD = "\033[1m"
CYAN = "\033[1;36m" # default color
GREEN = "\033[1;32m"
MAGENTA = "\033[38;2;255;0;144m"
PURPLE = "\033[1;35m"
RED = "\033[1;31m"
RESET = "\033[0m"
YELLOW = "\033[1;33m"
#endregion

# region --- Logo & UI Functions ---

# Store your custom ASCII logo here so it can be printed cleanly at startup
OMEGAZYPH_LOGO = r"""
   ___  __  __ _____ ____    _   ______     ______  _   _
  / _ \|  \/  | ____/ ___|  / \  |__  /\ \ / /  _ \| | | |
 | | | | |\/| |  _|| |  _  / _ \   / /  \ V /| |_) | |_| |
 | |_| | |  | | |__| |_| |/ ___ \ / /_   | | |  __/|  _  |
  \___/|_|  |_|_____\____/_/   \_/____|  |_| |_|   |_| |_|
                        OMEGAZYPH
"""


def print_logo(logo_text=OMEGAZYPH_LOGO, color=PURPLE):
    """Print the startup logo using the typing effect and color formatting."""
    # Print each line of the logo so multi-line ASCII art renders cleanly
    for line in logo_text.splitlines():
        if line:
            print_color(f"{BOLD}{color}{line}{RESET}")

# created typing effict
def print_color(text, color=CYAN):
    """Print text one character at a time with a short delay for a typing effect."""
    # Apply the selected ANSI color before writing characters
    sys.stdout.write(color)
    # Write each character and flush stdout immediately so delays appear live
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)
    # Reset text attributes and end the line
    print(RESET)

def print_ascii_banner(banner_title="Default Title Starting"):
    """Prints a dynamically centered starting ASCII banner."""
    # Set the total character width for the banner border
    total_width = 65
    # Calculate leading spaces needed to center the title inside the banner width
    title_length = len(banner_title)
    padding = (total_width - title_length) // 2

    # Generate the exact amount of leading spaces for centering
    spaces = " " * padding

    # Build the horizontal border line
    separator_line = "=" * total_width

    # Print the top border, centered title, and bottom border using the typing effect
    print_color(f"{PURPLE}{separator_line}{RESET}")
    print_color(f"{BOLD}{BLUE}{spaces}{banner_title}{RESET}")
    print_color(f"{PURPLE}{separator_line}{RESET}")

    
def print_message(message_type, message_text=""):
    """Unified message printing function using ANSI color formatting."""
    # Choose the prefix marker and ANSI color based on the message type
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
        # Print plain text when the message type does not match a known category
        print(message_text)
# endregion

# region --- Main Process ---

def main():
    #clears the screen
    os.system('cls' if os.name == 'nt' else 'clear') 

    # Display the startup banner
    print_logo()
    print_ascii_banner("Smart Backup")

    # In VS Code, the 'Current Working Directory' can sometimes be the root 
    # folder of your workspace. This line ensures we find the script's actual folder.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    source_folder = os.path.join(script_dir, "my_files")
    backup_folder = os.path.join(script_dir, "backup_folder")

    # Safety check: Ensure the source exists
    if not os.path.exists(source_folder):
        print_message("error",f"Error: Folder '{source_folder}' not found.")
        return

    # Create backup folder if missing
    if not os.path.exists(backup_folder):
        try:
            os.makedirs(backup_folder)
            print_message("status",f"Created new backup folder at: {backup_folder}")
        except OSError as error:
            print_message("error", f"could not make back_up folder. {error}")
            return

    files = os.listdir(source_folder)
    copied_count = 0
    skipped_count = 0
    failed_count = 0

    # Logic: Only copy if file is new or modified
    for file_name in files:
        source_path = os.path.join(source_folder, file_name)
        dest_path = os.path.join(backup_folder, file_name)

        if os.path.isfile(source_path):
            try:
                if os.path.exists(dest_path) and os.path.getmtime(source_path) <= os.path.getmtime(dest_path):
                    skipped_count += 1
                    continue 
            
                shutil.copy2(source_path, dest_path)
                copied_count += 1
                print_message("success",f"Updated: {file_name}")
            
            except OSError as error:
                failed_count +=1
                print_message("error",f"Failed to process '{file_name}': {error}")

    # Summary Output
    print_message("success",f"Files Updated: {copied_count}")
    print_message("warning",f"Files Skipped: {skipped_count}")
    if failed_count > 0:
        print_message("error", f"Files Failed: {failed_count}")
    
    # Ending banner
    print_ascii_banner("BACKUP COMPLETE")
# endregion

if __name__ == "__main__":
    main()