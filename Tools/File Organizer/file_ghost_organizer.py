#! /bin/env python

###############################################################################
# Date: 2026-01-07
# Script Name: file_ghost_organizer.py
# Author: omegazyph
# Updated: 2026-11-21
# Description: Automatically sorts the Downloads folder into categorized
#              subfolders to keep the Legion C: drive optimized.
###############################################################################

# --- Imports ---
# Import JSON parsing utilites to load folder and extension rules from disk
import json

# Import operating system interface utilities for paths, directories, and screen clearing
import os

# Import high-level file operations for moving files between directories
import shutil

# Import standard output and flush controls for typewriter text output
import sys

# Import time utilities for character delays and status pauses
import time

# --- ANSI Color Codes ---
# Define bold ANSI escape sequences for colored terminal output
BLUE = "\033[1;34m"
BOLD = "\033[1m"
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
PURPLE = "\033[1;35m"
RED = "\033[1;31m"
RESET = "\033[0m"
YELLOW = "\033[1;33m"


# --- UI Functions ---
def print_hacker(text, color=CYAN):
    """Print text character by character with a short delay for a typewriter effect."""
    # Set the active ANSI color before writing characters
    sys.stdout.write(color)
    # Write each character individually and flush immediately to the terminal
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)
    # Reset formatting and move to the next line
    print(RESET)


def print_ascii_banner(banner_title="Default Title Starting"):
    """Print a dynamically centered starting ASCII banner."""
    # Set the total width of the banner border
    total_width = 65
    # Measure the title length to calculate centered padding
    title_length = len(banner_title)
    padding = (total_width - title_length) // 2

    # Generate the exact number of leading spaces needed to center the title
    spaces = " " * padding

    # Build the horizontal border line
    separator_line = "=" * total_width

    # Print the top border, centered title, and bottom border
    print_hacker(f"{PURPLE}{separator_line}{RESET}")
    print_hacker(f"{BOLD}{BLUE}{spaces}{banner_title}{RESET}")
    print_hacker(f"{PURPLE}{separator_line}{RESET}")


def print_ascii_ending(ending_title="Default Title Ending"):
    """Print a dynamically centered closing ASCII banner."""
    # Set the total width of the closing banner border
    total_width = 65
    # Measure the ending title length to calculate centered padding
    title_length = len(ending_title)
    padding = (total_width - title_length) // 2

    # Generate the exact number of leading spaces needed to center the title
    spaces = " " * padding

    # Build the horizontal border line
    separator_line = "=" * total_width

    # Print the top border, centered ending title, and bottom border
    print_hacker(f"{PURPLE}{separator_line}{RESET}")
    print_hacker(f"{BOLD}{BLUE}{spaces}{ending_title}{RESET}")
    print_hacker(f"{PURPLE}{separator_line}{RESET}")


def print_message(message_type, message_text=""):
    """Unified message printing function using ANSI color formatting."""
    # Select the prefix symbol and ANSI color based on the message category
    if message_type == "error":
        print(f"{BOLD}{RED}[X] {message_text}{RESET}")
    elif message_type == "info":
        print(f"{BOLD}{BLUE}[*] {message_text}{RESET}")
    elif message_type == "status":
        print(f"{BOLD}{CYAN}[*] {message_text}{RESET}")
    elif message_type == "success":
        print(f"{BOLD}{GREEN}[+] {message_text}{RESET}")
    elif message_type == "warning":
        print(f"{BOLD}{YELLOW}[!] {message_text}{RESET}")
    else:
        # Print plain text if no recognized message type is supplied
        print(message_text)

def load_destinations(config_file_path):
    '''Load category-to-extension mapping from a JSON configuration file'''
    # Read and parse the JSON configuration using UTF-8 encoding
    with open(config_file_path, "r", encoding="utf-8") as json_file_handle:
        loaded_data = json.load(json_file_handle)

    # Normalize all configured extensions to lowercase for reliable matching
    normalized_destinations = {}
    for category_name, extension_list in loaded_data.items():
        normalized_destinations[category_name] = [
            ext.lower() for ext in extension_list
        ]
    return normalized_destinations

# --- Main Process ---
def organize_downloads():
    """Scan the user's Downloads folder and move matching files into category folders."""
    # Clear the terminal screen across Windows and Unix-like shells
    os.system('cls')  # Clear screen on Windows
    os.system('clear')  # Clear screen on Linux and macOS

    # Display the startup banner for the file organizer
    print_ascii_banner("OMEGAZYPH FILE GHOST: DOWNLOADS RECLAMATION")

    # Locate destinations.json in the same directory as this script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_directory, "destinations.json")


    # Load destinaton rules form JSON and exit cleanly if missing or invalid
    try:
        destinations = load_destinations(config_file_path)
    except (OSError, json.JSONDecodeError) as config_error:
        print_message("error", f"[ERROR] Failed to load destinations.json: {config_error}")

    # Resolve the full path to the current user's Downloads directory
    download_path = os.path.expanduser("~/Downloads")

    # Inform the user that directory scanning is starting
    print_hacker(f"[*] SCANNING: {download_path}")
    time.sleep(1)

    # Track how many files are successfully moved
    count = 0

    # Iterate over every entry inside the Downloads folder
    for filename in os.listdir(download_path):
        # Extract the normalized lowercase file extension
        file_ext = os.path.splitext(filename)[1].lower()

        # Check each category to see if this file extension matches
        for category, extensions in destinations.items():
            if file_ext in extensions:
                # Build the target subfolder path inside Downloads
                dest_folder = os.path.join(download_path, category)

                # Create the category subfolder if it does not already exist
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)

                # Attempt to move the file into its destination subfolder
                try:
                    shutil.move(
                        os.path.join(download_path, filename),
                        os.path.join(dest_folder, filename)
                    )
                    print_message("status", f"[MOVING] {filename} -> {category}")
                    count += 1
                except OSError as error:
                    # Print the file name and OS error reason if moving fails
                    print_message("error",f"[ERROR] Could not move {filename}: {error}")

    # Display the closing banner with the total count of organized files
    print_ascii_ending(f"{count} FILES CATEGORIZED AND RECLAIMED.")


# Run the main organizer function only when executed directly as a script
if __name__ == "__main__":
    organize_downloads()