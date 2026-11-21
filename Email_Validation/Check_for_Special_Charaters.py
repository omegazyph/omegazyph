#!/usr/bin/env python

# ==============================================================================
# 
# Script Name:  Check for Special characters
# Author:       omegazyph
# Date Created: 2026-08-21
# Date Updated: 2026-11-20
# Description:  Interactive command-line script that validates an email address
#               against a regular expression pattern for allowed characters and
#               domain format, styled with ANSI colors, banners, and status
#               messages.
# ==============================================================================

# --- Imports ---
import re

# --- ANSI Color Codes ---
BLUE = "\033[1;34m"  # Bold blue color escape sequence
BOLD = "\033[1m"  # Bold text escape sequence
CYAN = "\033[1;36m"  # Bold cyan color escape sequence
GREEN = "\033[1;32m"  # Bold green color escape sequence
PURPLE = "\033[1;35m"  # Bold purple color escape sequence
RED = "\033[1;31m"  # Bold red color escape sequence
RESET = "\033[0m"  # Reset text formatting back to default
YELLOW = "\033[1;33m"  # Bold yellow color escape sequence


# --- User Interface Functions ---


def print_ascii_banner(banner_title="Default Title Starting"):
    """Print a dynamically centered starting ASCII banner."""
    total_width = 80  # Total width of the banner border in characters
    title_length = len(banner_title)  # Length of the provided title string
    padding = (total_width - title_length) // 2  # Left spacing to center title

    # Build the exact number of leading spaces needed to center the title.
    leading_spaces = " " * padding  # Leading space characters
    border_line = "=" * total_width  # Horizontal separator line

    print(f"{PURPLE}{border_line}{RESET}")  # Print top border line
    print(f"{BOLD}{BLUE}{leading_spaces}{banner_title}{RESET}")  # Print centered title
    print(f"{PURPLE}{border_line}{RESET}")  # Print bottom border line


def print_ascii_ending(ending_title="Default Title Ending"):
    """Print a dynamically centered closing ASCII banner."""
    total_width = 80  # Total width of the banner border in characters
    title_length = len(ending_title)  # Length of the provided title string
    padding = (total_width - title_length) // 2  # Left spacing to center title

    # Build the exact number of leading spaces needed to center the title.
    leading_spaces = " " * padding  # Leading space characters
    border_line = "=" * total_width  # Horizontal separator line

    print(f"{PURPLE}{border_line}{RESET}")  # Print top border line
    print(f"{BOLD}{BLUE}{leading_spaces}{ending_title}{RESET}")  # Print centered title
    print(f"{PURPLE}{border_line}{RESET}")  # Print bottom border line


def print_message(message_type, message_text=""):
    """Print a formatted status message using ANSI color codes."""
    if message_type == "error":  # Format error messages in bold red
        print(f"{BOLD}{RED}[X] {message_text}{RESET}")
    elif message_type == "info":  # Format informational messages in bold blue
        print(f"{BOLD}{BLUE}[*] {message_text}{RESET}")
    elif message_type == "status":  # Format status messages in bold cyan
        print(f"{BOLD}{CYAN}[*] {message_text}{RESET}")
    elif message_type == "success":  # Format success messages in bold green
        print(f"{BOLD}{GREEN}[+] {message_text}{RESET}")
    elif message_type == "warning":  # Format warning messages in bold yellow
        print(f"{BOLD}{YELLOW}[!] {message_text}{RESET}")
    else:  # Print plain text when no matching type is given
        print(message_text)


# --- Main Application Logic ---


def main():
    """Run the regular expression email check inside the styled banner layout."""
    # Show the opening banner for the tool.
    print_ascii_banner("Check for Special Characters")  # Display startup banner

    # Prompt the user for an email address and remove outer whitespace.
    user_email = input("Enter your Email: ").strip()

    # Regular expression matching standard username characters, '@', domain
    # characters, a literal dot, and a top-level domain of at least 2 letters.
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    # Evaluate the input string against the regular expression pattern.
    if re.match(email_pattern, user_email):
        print_message("success", "Valid Email")  # Print green success message
    else:
        print_message("error", "Invalid Email")  # Print red error message

    # Show the closing banner at the end of execution.
    print_ascii_ending("Check for Special Characters Complete")  # Display closing banner


if __name__ == "__main__":
    main()