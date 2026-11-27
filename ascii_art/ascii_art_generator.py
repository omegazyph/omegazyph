#!/usr/bin/env python

# ======================================================================
# Date:           2026-09-08
# Script Name:    ascii_art1_3.py
# Author:         omegazyph
# Updated:        2026-11-27
# Description:    Generates ASCII art banners with an expanded interactive
#                 menu to choose fonts while keeping banner text across loops.
# File Structure: ascii_art_project/
#                     ascii_art1_3.py
# ======================================================================


# region --- Imports ---

# Import standard output and flush controls for character-by-character output
import sys

# Import time utilities for character delays during typewriter printing
import time

# Import pyfiglet for rendering ASCII art text banners
import pyfiglet

# endregion


# region --- ANSI Color Codes ---

# Define bold ANSI escape sequences for colored terminal output
BLUE = "\033[1;34m"
BOLD = "\033[1m"
CYAN = "\033[1;36m"  # default color
GREEN = "\033[1;32m"
MAGENTA = "\033[38;2;255;0;144m"
PURPLE = "\033[1;35m"
RED = "\033[1;31m"
RESET = "\033[0m"
YELLOW = "\033[1;33m"

# endregion


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
        else:
            print("Can't load Logo")


def print_color(text, color=CYAN):
    """Print text one character at a time with a short delay for a typing effect."""
    # Apply the selected ANSI color before writing characters
    sys.stdout.write(color)
    # Write each character and flush stdout immediately so delays appear live
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.01)
    # Reset text attributes and end the line
    print(RESET)


def print_ascii_banner(banner_title="Default Title Starting"):
    """Print a dynamically centered ASCII banner with top and bottom borders."""
    # Set the total character width for the banner border
    total_width = 65
    # Calculate leading spaces needed to center the title inside the banner width
    title_length = len(banner_title)
    padding = 0
    if total_width > title_length:
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
    """Print formatted messages using prefix markers and ANSI color codes."""
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
    """Run the interactive ASCII art generator with an expanded font menu."""
    # Display the startup logo first before the tool banner
    print_logo()
    print_ascii_banner("ASCII art")

    # Define expanded font options mapping menu numbers to pyfiglet font names and labels
    available_fonts = {
        "1": ("slant", "Slant"),
        "2": ("standard", "Standard"),
        "3": ("banner3-D", "3D Banner"),
        "4": ("block", "Block"),
        "5": ("digital", "Digital"),
        "6": ("big", "Big"),
        "7": ("doom", "Doom"),
        "8": ("larry3d", "Larry 3D"),
        "9": ("rectangles", "Rectangles"),
        "10": ("small", "Small"),
    }

    # Prompt once outside the loop so user_text stays the same across font previews
    user_text = input("Enter the text for your banner: ")

    # Repeat font selection and banner rendering until the user chooses to stop
    keep_running = True
    while keep_running:
        # Display font choices
        print("\nSelect a font style:")
        for key, font_info in available_fonts.items():
            print(key + ". " + font_info[1])

        # Get font choice
        choice = input("\nEnter choice (1-10): ").strip()

        # Determine chosen font, defaulting to 'slant' if selection is invalid
        if choice in available_fonts:
            selected_font = available_fonts[choice][0]
        else:
            print("\nInvalid choice. Defaulting to 'slant' font.")
            selected_font = "slant"

        # Generate and print ASCII art
        print("\n")
        try:
            banner_art = pyfiglet.figlet_format(user_text, font=selected_font)
            print(banner_art)
        except pyfiglet.FontNotFound:
            print_message("warning", f"Font '{selected_font}' not found. Using 'slant'.")
            banner_art = pyfiglet.figlet_format(user_text, font="slant")
            print(banner_art)

        # Ask whether to try another font with the same banner text
        repeat_choice = input("Would you like to try another font? (y/n): ").strip().lower()
        if repeat_choice == "y" or repeat_choice == "yes":
            keep_running = True
        else:
            keep_running = False

    print_ascii_banner("Thank you for using ASCII art")

# endregion


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)