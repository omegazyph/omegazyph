#!/usr/bin/env python

# ==========================================================================================
# Date:         2026-09-22
# Script Name:  python_starter.py
# Author:       omegazyph
# Updated:      2026-11-23
# Description:  Core library providing ANSI colors, unified messaging,
#               and dynamically centered ASCII banners.
# ===========================================================================================

# region --- Imports ---

# Import operating system interface helpers for clearing the terminal screen
import os

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
PURPLE = "\033[1;35m"
RED = "\033[1;31m"
RESET = "\033[0m"
YELLOW = "\033[1;33m"
#endregion

#region --- UI Functions ---
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
        print_color(f"{BOLD}{CYAN}[*] {message_text}{RESET}")
    elif message_type == "success":
        print_color(f"{BOLD}{GREEN}[+] {message_text}{RESET}")
    elif message_type == "warning":
        print_color(f"{BOLD}{YELLOW}[!] {message_text}{RESET}")
    else:
        # Print plain text when the message type does not match a known category
        print(message_text)
#endregion

#region --- Main Process ---
def main():
    """Main execution entry point."""
    #clears the screen
    os.system('cls' if os.name == 'nt' else 'clear') 
    
    # Display the startup banner
    print_ascii_banner("Put your Title here")

    # Execute operational status messages
    print_message("status", "Scanning for active devices on your network")
    print_message("info", "this is a info line")
    print_message("warning", "Please wait, this may take a few seconds")
    print_message("success", "Scan complete!")
    print_message("error", "No devices detected.")

    # Displaying the ending banner
    print_ascii_banner("Put your ending title here")
#endregion

# Run main only when the file is executed directly rather than imported
if __name__ == "__main__":
    main()