#!/usr/bin/env python

#===========================================================================
# Date: 2026-11-19
# Script Name: install_requirements.py
# Author: omegazyph
# Updated: 2026-11-19
# Description: Verifies that the pyserial library is installed in the active
#             Python environment and installs it via pip if it is missing.
#===========================================================================

# --- Imports ---
import subprocess
import sys

# --- ANSI Color Codes ---
BLUE = "\033[1;34m"
BOLD = "\033[1m"
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
PURPLE = "\033[1;35m"
RED = "\033[1;31m"
RESET = "\033[0m"
YELLOW = "\033[1;33m"


# --- UI Functions ---
def print_ascii_banner(banner_title="Default Title Starting"):
    """Prints a dynamically centered starting ASCII banner."""
    total_width = 80
    title_length = len(banner_title)
    padding = (total_width - title_length) // 2

    # Generate the exact amount of leading spaces for centering
    spaces = " " * padding

    separator_line = "=" * total_width

    print(f"{PURPLE}{separator_line}{RESET}")
    print(f"{BOLD}{BLUE}{spaces}{banner_title}{RESET}")
    print(f"{PURPLE}{separator_line}{RESET}")


def print_ascii_ending(ending_title="Default Title Ending"):
    """Prints a dynamically centered closing ASCII banner."""
    total_width = 80
    title_length = len(ending_title)
    padding = (total_width - title_length) // 2

    # Generate the exact amount of leading spaces for centering
    spaces = " " * padding

    separator_line = "=" * total_width

    print(f"{PURPLE}{separator_line}{RESET}")
    print(f"{BOLD}{BLUE}{spaces}{ending_title}{RESET}")
    print(f"{PURPLE}{separator_line}{RESET}")


def print_message(message_type, message_text=""):
    """Unified message printing function using ANSI color formatting."""
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


def check_and_install_pyserial() -> None:
    """Checks for pyserial and installs it if not already present."""
    try:
        import serial
        print_message("success","The 'pyserial' package is already installed.")
        return True
    
    except ImportError as import_error:
        print_message("warning",f"'pyserial' was not found ({import_error}).")
        user_response = input("Do you want to install 'pyserial' now? (yes/no):").strip().lower()
        if user_response not in ("y","yes"):
            print_message("info","Installation cancelled by user.")
            return False

        install_succeeded = False

        try:
            # perform the install
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "pyserial"], 
                check=True,
            )
            install_succeeded = True

        except subprocess.CalledProcessError as process_error:
            print_message(
                "error",
                f"pip failed with exit code {process_error.returncode} while installing 'pyserial'",
            )
            return False

        except FileNotFoundError as missing_executable_error:
                    print_message(
                        "error",
                        f"Python or pip excutable was not found: {missing_executable_error}",
                    )
                    return False

        except OSError as operating_system_error:
                    print_message(
                        "error",
                        f"Operating system error during install: {operating_system_error}",
                    )
                    return False

        except Exception as unexpected_error:
                    print_message(
                        "error",
                        f"Unexpected error during install: {unexpected_error}",
                    )
                    return False

        if install_succeeded:
            try:
                import serial
                print_message("success", "The 'pyserial' package has been installed and verified.")
                return True
            
            except ImportError as verify_error:
                print_message(
                    "error",
                    f"'pyserial' appeared to install, but importing 'serial' failed: {verify_error}",
                )
                return False
        print_message("info","Test run complete with no package installed.")
        return False
    
    except Exception as unexpected_import_error:
        print_message(
            "error",
            f"Unexpected error while chaecking for 'pyserial': {unexpected_import_error}",
        )
        return False

# --- Main Process ---
def main() -> None:
    # Main entry point for requirement checking.
    # Displays the startup Banner
    print_ascii_banner("GMC Requirements for Read GMC Codes")

    requirements_ok = check_and_install_pyserial()

    print_ascii_ending("Requirements Check Complete")

    if requirements_ok:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
