#!/usr/bin/env python

# =============================================================================
# Date:           2026-01-07
# Script Name:    aether_briefing.py
# Author:         Omegazyph
# Updated:        2026-11-23
# Description:    Scrapes top Hacker News headlines and local IP-based weather
#                 to provide a daily terminal briefing.
# File Structure: project_root/
#                     aether_briefing.py
# =============================================================================

#region --- Imports ---

# Import json module for optional future external configuration loading
# import json

# Import operating system interface module for clearing the terminal screen
import os

# Import standard output stream module for character-by-character output control
import sys

# Import time module for typing delays, pauses between items, and timestamps
import time

# Import requests module for performing HTTP GET requests to external APIs
import requests

#endregion

# region --- ANSI Color Codes ---
# Define ANSI escape sequences for terminal colors and bold/reset formatting
BLUE = "\033[1;34m"
BOLD = "\033[1m"
CYAN = "\033[1;36m"  # Default color used when no color argument is passed
GREEN = "\033[1;32m"
MAGENTA = "\033[38;2;255;0;144m"  # 24-bit RGB magenta for active status lines
PURPLE = "\033[1;35m"
RED = "\033[1;31m"
RESET = "\033[0m"
YELLOW = "\033[1;33m"
# endregion

# region --- UI Functions ---
def print_color(text, color=CYAN):
    """Print text one character at a time with a short delay for a typing effect."""
    # Apply the selected ANSI escape color before writing any characters
    sys.stdout.write(color)

    # Write each character individually and flush stdout so the delay is visible
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.01)

    # Reset terminal text formatting and finish the line with a newline
    print(RESET)


def print_ascii_banner(banner_title="Default Title Starting"):
    """Print a dynamically centered ASCII banner with top and bottom borders."""
    # Set the total character width used for the top and bottom border lines
    total_width = 65

    # Calculate how many leading spaces are needed to center the title text
    title_length = len(banner_title)
    padding = (total_width - title_length) // 2

    # Build the leading space string and horizontal separator line
    spaces = " " * padding
    separator_line = "=" * total_width

    # Print the top purple border, centered bold blue title, and bottom border
    print_color(f"{PURPLE}{separator_line}{RESET}")
    print_color(f"{BOLD}{BLUE}{spaces}{banner_title}{RESET}")
    print_color(f"{PURPLE}{separator_line}{RESET}")


def print_message(message_type, message_text=""):
    """Print formatted messages with distinct prefixes and colors by message type."""
    # Match the requested message_type to its corresponding tag and color
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
        # Fall back to standard uncolored printing for unknown message types
        print(message_text)
# endregion

# region --- Briefing Data Functions ---
def get_tech_news():
    """Fetch and print the top five Hacker News story titles."""
    # Notify the user that the script is connecting to the Hacker News API
    print_message("status", "PROBING HACKER NEWS UPLINK...\n")
    try:
        # Request the list of top story IDs with a 10-second timeout guard
        response = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            timeout=10,
        )
        # Raise an HTTPError if the server returned a non-2xx status code
        response.raise_for_status()

        # Slice the first five story IDs from the returned JSON array
        top_ids = response.json()[:5]

        # Display a section banner before listing headlines
        print_ascii_banner("--- TOP TECH HEADLINES ---")

        # Fetch and display each story's details one by one
        for item_id in top_ids:
            # Request individual item metadata with a 10-second timeout
            item_response = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json",
                timeout=10,
            )
            # Ensure the individual item request succeeded before parsing JSON
            item_response.raise_for_status()

            # Parse the story object and print its title as an info message
            item = item_response.json()
            print_message("info", f"{item['title']}\n")

            # Brief pause between items for readability
            time.sleep(0.2)

    # Catch network/request errors as well as malformed JSON or missing dictionary keys
    except (requests.RequestException, ValueError, KeyError, TypeError) as error:
        print_message("error", f"NEWS UPLINK FAILED: {error}\n")


def get_universal_weather():
    """Fetch current weather conditions using IP-based automatic location."""
    # Omitting a city lets wttr.in estimate location from the request IP address
    print_message("status", "SCANNING LOCAL GEOLOCATION...")
    try:
        # Request compact single-line weather output with a 10-second timeout
        response = requests.get("https://wttr.in/?format=4", timeout=10)

        # Verify HTTP 200 OK before stripping whitespace and printing output
        if response.status_code == 200:
            weather_data = response.text.strip()
            print_message("info", f"LOCATION ESTABLISHED: {weather_data}\n")
        else:
            print_message("error", "WEATHER SERVER UNREACHABLE")

    # Catch network, connection, and timeout errors raised by requests
    except requests.RequestException as network_error:
        print_message("error", f"UPLINK ERROR: CHECK INTERNET CONNECTION ({network_error})\n")
# endregion

# region --- Main Process ---
def main():
    """Run the Aether daily terminal briefing workflow."""
    # Clear the console screen on both Windows ('nt') and Unix-like systems
    os.system("cls" if os.name == "nt" else "clear")

    # Print the AETHER header block, connection status, and current timestamp
    print_color(f"{PURPLE}======================================================{RESET}")
    print_color(f"{BOLD}{BLUE}    ___    __________________  ________  ____     {RESET}")
    print_color(f"{BOLD}{BLUE}   /   |  / ____/_  __/ / / / ____/ __ \\/ / /     {RESET}")
    print_color(f"{BOLD}{BLUE}  / /| | / __/   / / / /_/ / __/ / /_/ / / /      {RESET}")
    print_color(f"{BOLD}{BLUE} / ___ |/ /___  / / / __  / /___/ _, _/_/_/       {RESET}")
    print_color(f"{BOLD}{BLUE}/_/  |_/_____/ /_/ /_/ /_/_____/_/ |_(_|_)       {RESET}")
    print_color(f"{PURPLE}======================================================{RESET}")
    print_color(f"{BOLD}{MAGENTA} STATUS: SECURE CONNECTION ESTABLISHED{RESET}")
    print_color(f"{BOLD}{BLUE} DATE:   {time.strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    print_color(f"{PURPLE}======================================================\n{RESET}")

    # Run the news and weather briefing sections in sequence
    get_tech_news()
    get_universal_weather()

    # Print the closing banner to signal completion
    print_ascii_banner("BRIEFING COMPLETE. SYSTEM READY FOR CODING.")
# endregion

# Only run main() when this script is executed directly, not when imported
if __name__ == "__main__":
    main()