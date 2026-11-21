#!/usr/bin/env python

# ==============================================================================
# Script Name:  Basic Email Validation
# Author:       omegazyph
# Date Created: 2026-08-21
# Date Updated: 2026-11-20
# Description:  Basic command-line script to check if user input contains an
#               at sign and a period, styled with ANSI colors, banners, and
#               unified status messages.
# ==============================================================================

# --- ANSI Color Codes ---
BLUE = "\033[1;34m"
BOLD = "\033[1m"
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
PURPLE = "\033[1;35m"
RED = "\033[1;31m"
RESET = "\033[0m"
YELLOW = "\033[1;33m"


# --- User Interface Functions ---


def print_ascii_banner(banner_title="Default Title Starting"):
    """Print a dynamically centered starting ASCII banner."""
    total_width = 80
    title_length = len(banner_title)
    padding = (total_width - title_length) // 2

    # Build the exact number of leading spaces needed to center the title.
    leading_spaces = " " * padding
    border_line = "=" * total_width

    print(f"{PURPLE}{border_line}{RESET}")
    print(f"{BOLD}{BLUE}{leading_spaces}{banner_title}{RESET}")
    print(f"{PURPLE}{border_line}{RESET}")


def print_ascii_ending(ending_title="Default Title Ending"):
    """Print a dynamically centered closing ASCII banner."""
    total_width = 80
    title_length = len(ending_title)
    padding = (total_width - title_length) // 2

    # Build the exact number of leading spaces needed to center the title.
    leading_spaces = " " * padding
    border_line = "=" * total_width

    print(f"{PURPLE}{border_line}{RESET}")
    print(f"{BOLD}{BLUE}{leading_spaces}{ending_title}{RESET}")
    print(f"{PURPLE}{border_line}{RESET}")


def print_message(message_type, message_text=""):
    """Print a formatted status message using ANSI color codes."""
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
        print(message_text)


# --- Main Application Logic ---


def main():
    """Run the basic email check inside the styled banner layout."""
    # Show the opening banner for the tool.
    print_ascii_banner("Basic Email Validation")

    # Prompt the user for an email address and remove outer whitespace.
    user_email = input("Enter your Email: ").strip()

    # Perform the basic check for both '@' and '.' characters.
    if "@" in user_email and "." in user_email:
        print_message("success", "Valid Email")
    else:
        print_message("error", "Invalid Email")

    # Show the closing banner at the end of execution.
    print_ascii_ending("Validation Complete")


if __name__ == "__main__":
    main()