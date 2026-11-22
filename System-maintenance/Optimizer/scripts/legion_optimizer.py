#! /bin/env python

#===========================================================================
# Date: 2026-01-07
# Script Name: legion_optimizer.py
# Author: omegazyph
# Updated: 2026-11-21
# Description: Fixed system optimization with stable Battery diagnostics.
#==============================================================================


# --- Imports ---
# Import ctypes to interface with Windows DLL functions for checking and requesting Administrator privileges
import ctypes

# Import operating system utilities for clearing the terminal screen, checking platform type, and reading environment variables
import os

# Import shutil to locate external system binaries such as 'sudo' on POSIX systems
import shutil

# Import subprocess to execute system maintenance commands, capture output, and quote command-line arguments
import subprocess

# Import system-specific parameters and standard output stream controls for live terminal rendering
import sys

# Import time utilities for character typing delays and brief diagnostic pauses
import time

# Import psutil to retrieve hardware sensor information such as battery charge percentage and AC power status
import psutil

# --- ANSI Color Codes ---
# Define bold ANSI escape sequences for colored terminal output
BLUE = "\033[1;34m"
BOLD = "\033[1m"
CYAN = "\033[1;36m"  # Default color
GREEN = "\033[1;32m"
PURPLE = "\033[1;35m"
RED = "\033[1;31m"
RESET = "\033[0m"
YELLOW = "\033[1;33m"


# --- UI and Privilege Functions ---
# Verify and request elevated Administrator (Windows) or root (Linux) privileges
def ensure_elevated():
    """Ensure the script is running with Administrator privileges on Windows or root on Linux."""
    # Check if the script is running on a Windows operating system
    if os.name == "nt":
        try:
            # Query the Windows Shell API to verify whether the current process has Administrator rights
            is_admin = bool(ctypes.windll.shell32.IsUserAnAdmin())
        except (AttributeError, OSError) as admin_check_error:
            # Report any error encountered while checking Windows Administrator status
            print_message("error", f"Unable to verify Windows Admin status: {admin_check_error}")
            return False

        # Return immediately if the script is already running with Administrator privileges
        if is_admin:
            return True

        # Safely quote the script path and command-line arguments so spaces in paths are preserved
        script_arguments = subprocess.list2cmdline(sys.argv)

        try:
            # Trigger a Windows User Account Control (UAC) prompt to relaunch Python as Administrator
            elevation_result = ctypes.windll.shell32.ShellExecuteW(
                None,
                "runas",
                sys.executable,
                script_arguments,
                None,
                1,
            )
            # ShellExecuteW returns a value greater than 32 when the elevated process launches successfully
            if elevation_result > 32:
                # Exit the original unprivileged process so only the elevated instance continues
                sys.exit(0)

            # Report if the user declined the UAC prompt or Windows failed to launch the elevated window
            print_message("error", "Administrator elevation was declined or could not be started.")
            return False
        except (AttributeError, OSError, SystemExit) as elevation_error:
            # Allow SystemExit to pass through normally when terminating the unprivileged parent process
            if isinstance(elevation_error, SystemExit):
                raise
            # Report any Windows API or operating system error during elevation
            print_message("error", f"Failed to elevate privileges on Windows: {elevation_error}")
            return False
            
    else:
        # On POSIX systems such as Linux, an effective user ID of 0 indicates root privileges
        if hasattr(os, "geteuid") and os.geteuid() == 0:
            return True

        # Locate the 'sudo' executable in the system PATH
        sudo_path = shutil.which("sudo")
        if not sudo_path:
            # Report an error if root access is needed but 'sudo' is unavailable
            print_message("error", "Root privileges are required, and 'sudo' was not found.")
            return False

        try:
            # Replace the current process image with an elevated 'sudo python <script> <args>' process
            os.execvp(sudo_path, [sudo_path, sys.executable] + sys.argv)
        except OSError as sudo_error:
            # Report if executing 'sudo' fails at the operating system level
            print_message("error", f"Failed to elevate with sudo: {sudo_error}")
            return False

    # Default fallback return if elevation could not be confirmed
    return False


# Create a character-by-character typing effect in the terminal
def print_hacker(text, color=CYAN):
    """Print text one character at a time with a short delay for a typing effect."""
    # Apply the selected ANSI color before writing characters
    sys.stdout.write(color)
    # Write each character and flush stdout immediately so delays appear live
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)
    # Reset ANSI formatting and move to the next line
    print(RESET)


# Print a centered startup ASCII banner
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
    print_hacker(f"{PURPLE}{separator_line}{RESET}")
    print_hacker(f"{BOLD}{BLUE}{spaces}{banner_title}{RESET}")
    print_hacker(f"{PURPLE}{separator_line}{RESET}")


# Print a centered closing ASCII banner
def print_ascii_ending(ending_title="Default Title Ending"):
    """Prints a dynamically centered closing ASCII banner."""
    # Set the total character width for the closing banner border
    total_width = 65
    # Calculate leading spaces needed to center the ending title
    title_length = len(ending_title)
    padding = (total_width - title_length) // 2

    # Generate the exact amount of leading spaces for centering
    spaces = " " * padding

    # Build the horizontal border line
    separator_line = "=" * total_width

    # Print the top border, centered ending title, and bottom border using the typing effect
    print_hacker(f"{PURPLE}{separator_line}{RESET}")
    print_hacker(f"{BOLD}{BLUE}{spaces}{ending_title}{RESET}")
    print_hacker(f"{PURPLE}{separator_line}{RESET}")


# Print status, warning, success, info, or error messages with standardized prefixes and colors
def print_message(message_type, message_text=""):
    """Unified message printing function using ANSI color formatting."""
    # Choose the prefix marker and ANSI color based on the message type
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
        # Print plain text when the message type does not match a known category
        print(message_text)


# Retrieve current battery charge percentage and AC power connection status
def get_battery_info():
    """Uses psutil for stable battery reporting."""
    # Query the system battery sensor through psutil
    battery = psutil.sensors_battery()
    # Extract percentage and human-readable power state if a battery is detected
    if battery:
        percent = battery.percent
        plugged = "Plugged In" if battery.power_plugged else "On Battery"
        return percent, plugged
    # Return None values when running on a desktop or system without a battery sensor
    return None, None

# --- Main Process ---
def optimize():
    """Execute privilege check, battery diagnostics, SSD trim, DNS flush, and temporary file cleanup."""
    # Verify elevated privileges before starting system maintenance tasks
    if not ensure_elevated():
        # Pause so the user can read the elevation error message before the window closes
        try:
            input("\nPress Enter to exit...")
        except EOFError:
            pass
        return

    # Clear the terminal screen for a clean workstation display
    os.system('cls' if os.name == 'nt' else 'clear')

    # Display the startup banner and pause briefly before running diagnostics
    print_ascii_banner("OMEGAZYPH LEGION COMMAND: STABLE DIAGNOSTIC")
    time.sleep(1)

    # 1. STABLE BATTERY CHECK
    # Query and display current battery charge and AC power state
    percent, status = get_battery_info()
    if percent is not None:
        print_message("status", f"Battery Level: {percent}%")
        print_message("status", f"Power Status: {status}")
    else:
        print_message("warning", "Battery Sensor not found.")

    # 2. ACTUAL OPTIMIZATION (Admin Required)
    # --- Drive Optimization / TRIM ---
    
    # --- SSD Trim ---
    try:
        # Notify the user that drive optimization is starting
        print("\n")
        print_message("info", "INITIATING SYSTEM TRIM...")

        if os.name == "nt":
            # Run Windows drive optimization (TRIM) on drive C: and raise an exception if it fails
            subprocess.run(
                "defrag C: /O",
                shell=True,
                capture_output=True,
                text=True,
                check=True,
        )
            # Confirm the drive opimization succeeded
            print_message("success", "Drive Optimization (TRIM) completed")
        else:
            # Verify 'fstrim' is installed on linux before running it
            fstrim_path = shutil.which("fstrim")
            if not fstrim_path:
                print_message("warning", "fstrim utility not found, skkpping Linux TRIM.")
            else:
                # Run filesystem Trim on the root mount on linux
                subprocess.run(
                    ["fstrim", "-v", "/"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                # Confirm that SSD optimization succeeded
                print_message("success", "SSD Optimization (Trim) completed.")

    except (subprocess.CalledProcessError) as trim_error:
        # Extract command output deails if available
        details = (trim_error.stderr or trim_error.stdout or "").strip()
        if "discard operation is not supported" in details.lower() or "not supported" in details.lower():
            # treat unsupported discard on vm/virtual/live filesystems as a non-fatal warning
            print_message("warning", f"Drive Trim skipped (not supported on target): {details}")
        else:
            print_message("error",f"Drive Trim failed: {details or trim_error}")
    except OSError as trim_os_error:
        # Report any OS-level error encounted during SSD/Drive Trim
        print_message("error", f"Drive Trim failed: {trim_os_error}")

    # --- DNS Flush ---
    try:
        # Notify the user that the DNS resolver cache flush is starting
        print("\n")
        print_message("warning", "INITIATING DNS FLUSH...")

        if os.name =="nt":
            # Flush the windows DNS Resolver cache
            subprocess.run(
                "ipconfig /flushdns",
                shell=True,
                capture_output=True,
                text=True,
                check=True,
            )
            # Conform that the DNS cache was cleared
            print_message("success", "Network DNS Cache cleared.")
        else:
            # Check if 'resolvectl' (systemed-resolved) is available on linux
            resolvectl_path = shutil.which("resolvectl")
            if not resolvectl_path:
                print_message("warning", "resolvectl not found (systemd-resolved not in use); DNS flush skipped.")
            else:
                subprocess.run(
                    ["resolvectl", "flush-caches"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                # Confirm that the DNS cache was cleared
                print_message("success", "Network DNS Cache cleared.")

    except (subprocess.CalledProcessError,OSError) as dns_error:
        # Extract standard error or standard output text from the failed ipconfig command
        details = ""
        if isinstance(dns_error, subprocess.CalledProcessError):
            details = (dns_error.stderr or dns_error.stdout or "").strip()
        if details:
            print_message("error", f"DNS Flush failed: {details}")
        else:
            print_message("error", f"DNS Flush failed: {dns_error}")

    # 3. Temporary File cleanup
    try:
        # Notify the user that temporary file cleanup is starting
        print("\n")
        print_message("warning", "INITIATING TEMP Purge...")

        if os.name == "nt":
            # Read the Windows TEMP directory path from environment variables
            temp_path = os.environ.get('TEMP')
            if not temp_path:
                raise OSError("TEMP environment variable is not set.")
            # Force-delete files inside the TEMP directory quietly and raise an exception on failure
            subprocess.run(
                f'del /q /f /s "{temp_path}\\*.*"',
                shell=True,
                capture_output=True,
                text=True,
                check=True,
            )
        else:
            # Clean temporary file inside /temp on linux while keeping the /tmp directory itself
            subprocess.run(
                "rm -rf /tmp/*",
                shell=True,
                capture_output=True,
                text=True,
                check=True,
            )
        # Confirm that temporary junk files were purged
        print_message("success", "Temporary junk files purged.")

    except (subprocess.CalledProcessError, OSError) as purge_error:
        # Extract command output details if available
        details = ""
        if isinstance(purge_error, subprocess.CalledProcessError):
            details = (purge_error.stderr or purge_error.stdout or "").strip()
        if details:
            print_message("error", f"Something went wrong in purge: {details}")
        else:
            print_message("error", f"Somethong went wrong in purge: {purge_error}")

    # Display the closing banner once all tasks have finished
    print_ascii_ending("SYSTEM OPTIMIZED | PROJECT: MATRIX_STATION ")

    # Pause before exiting so output stays visible if launched in a new window
    try:
        input("\nPress Enter to exit...")
    except EOFError:
        # Handle non-interactive runs where standard input is closed
        pass

# Entry point guard to run optimize() only when executed directly as a script
if __name__ == "__main__":
    optimize()