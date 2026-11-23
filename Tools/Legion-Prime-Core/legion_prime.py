#!/usr/bin/env python

# ===============================================================================
# Project Folder Structure:
#   Legion-Prime-Core/
#     ├── README.md
#     ├── launch_legion.bat
#     └── legion_prime.py
#
# Date:         2026-01-07
# Script Name:  legion_prime.py
# Author:       omegazyph
# Updated:      2026-11-23
# Description:  Combines system optimization, hardware diagnostics, location-aware
#               weather, top Hacker News headlines, and a network speed test.
# ===============================================================================


# region --- Imports ---
# Import os for screen clearing, platform detection, and path handling
import os

# Import subprocess for running external system maintenance utilities
import subprocess

# Import sys for writing output streams and flushing character delays
import sys

# Import time for typewriter output pacing
import time

# Import psutil for memory, battery, and disk usage diagnostics
import psutil

# Import requests for fetching weather and Hacker News data over HTTP
import requests

# endregion


# region --- ANSI Color Codes ---
# Define bold ANSI escape sequences for colored terminal output
BLUE = "\033[1;34m"
BOLD = "\033[1m"
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
PURPLE = "\033[1;35m"
RED = "\033[1;31m"
RESET = "\033[0m"
YELLOW = "\033[1;33m"
# endregion


# region --- UI Functions ---
def print_color(text, color=CYAN):
    """Print text one character at a time with a short delay for a typing effect."""
    # Apply the selected ANSI color before writing characters
    sys.stdout.write(color)
    # Write each character and flush standard output immediately so delays appear live
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.01)
    # Reset text attributes and end the line
    print(RESET)


def print_ascii_banner(banner_title="Default Title Starting"):
    """Print a dynamically centered starting ASCII banner."""
    # Set the total character width for the banner border
    total_width = 65
    # Calculate leading spaces needed to center the title inside the banner width
    title_length = len(banner_title)
    padding = (total_width - title_length) // 2

    # Generate the exact number of leading spaces for centering
    spaces = " " * padding

    # Build the horizontal border line
    separator_line = "=" * total_width

    # Print the top border, centered title, and bottom border using the typing effect
    print_color(f"{PURPLE}{separator_line}{RESET}")
    print_color(f"{BOLD}{BLUE}{spaces}{banner_title}{RESET}")
    print_color(f"{PURPLE}{separator_line}{RESET}")


def print_ascii_ending(ending_title="Default Title Ending"):
    """Print a dynamically centered closing ASCII banner."""
    # Set the total character width for the closing banner border
    total_width = 65
    # Calculate leading spaces needed to center the ending title
    title_length = len(ending_title)
    padding = (total_width - title_length) // 2

    # Generate the exact number of leading spaces for centering
    spaces = " " * padding

    # Build the horizontal border line
    separator_line = "=" * total_width

    # Print the top border, centered ending title, and bottom border using the typing effect
    print_color(f"{PURPLE}{separator_line}{RESET}")
    print_color(f"{BOLD}{BLUE}{spaces}{ending_title}{RESET}")
    print_color(f"{PURPLE}{separator_line}{RESET}")


def print_message(message_type, message_text=""):
    """Print status messages using standardized prefixes and ANSI colors."""
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
# endregion


# region --- Main Functions ---
def get_briefing():
    """Fetch current weather from wttr.in and top stories from Hacker News."""
    print_ascii_banner("INITIATING PROJECT AETHER: GLOBAL UPLINK")

    # 1. Universal Weather (Auto-Location via IP)
    try:
        # Request a compact one-line summary from wttr.in with a 5-second timeout
        response = requests.get("https://wttr.in/?format=4", timeout=5)
        response.raise_for_status()
        weather_text = response.text.strip()
        print_message("info", f"ENV: {weather_text}\n")
    except requests.exceptions.RequestException:
        print_message("error", "WEATHER UPLINK OFFLINE")

    # 2. Tech News (Top 3 Hacker News stories)
    try:
        # Fetch top story identifiers and limit to the first three items
        top_ids_response = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            timeout=5,
        )
        top_ids_response.raise_for_status()
        news_ids = top_ids_response.json()[:3]

        print_ascii_banner("--- Hacker News ---")
        for story_id in news_ids:
            # Fetch each story individually with its own timeout
            story_response = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                timeout=5,
            )
            story_response.raise_for_status()
            story_data = story_response.json() or {}
            title = story_data.get("title", "Untitled story")
            print_message("info", f"{title}\n")
    except (requests.exceptions.RequestException, ValueError):
        print_message("error", "NEWS UPLINK OFFLINE\n")


def run_optimizer():
    """Run Windows drive optimization and DNS cache flush, then report RAM usage."""
    print_ascii_banner("INITIATING LEGION OPTIMIZER: SYSTEM PURGE")

    if os.name == "nt":
        # SSD Trim / Drive Optimization on C:
        print_message("info", "OPTIMIZING SSD STORAGE...")
        try:
            subprocess.run(
                ["defrag", "C:", "/O"],
                capture_output=True,
                text=True,
                check=True,
            )
            print_message("success", "OPTIMIZER COMPLETED\n")
        except (subprocess.CalledProcessError, OSError) as trim_error:
            print_message("error", f"SSD TRIM FAILED: {trim_error}\n")

        # DNS Cache Flush
        print_message("info", "FLUSHING NETWORK CACHE...")
        try:
            subprocess.run(
                ["ipconfig", "/flushdns"],
                capture_output=True,
                text=True,
                check=True,
            )
            print_message("success", "DNS CACHE FLUSHED\n")
        
        except subprocess.CalledProcessError as dns_error:
            details = dns_error.stderr.strip() or str(dns_error)
            print_message("error", f"DNS FLUSH FAILED: {details}")
            print_message("warning", "Please use the Launch_Legion.bat for admin\n")
        
        except OSError as dns_error:
            print_message("error", f"DNS FLUSH FAILED: {dns_error}\n")
    else:
        print_message("warning", "WINDOWS MAINTENANCE COMMANDS SKIPPED ON NON-WINDOWS OS\n")

    # RAM Utilization Check
    memory_info = psutil.virtual_memory()
    print_message("info", f"RAM STABILITY: {memory_info.percent}% UTILIZED\n")


def check_hardware_health():
    """Check battery charge/charging status and free disk space."""
    print_ascii_banner("DIAGNOSING LEGION HARDWARE PULSE")

    # 1. Battery Health (guard against systems without a battery sensor)
    battery = psutil.sensors_battery()
    if battery is not None:
        status = "Charging" if battery.power_plugged else "Discharging"
        color = GREEN if battery.percent > 20 else RED
        print_color(f"[>] BATTERY: {battery.percent}% ({status})\n", color)
    else:
        print_message("error", "BATTERY SENSOR NOT DETECTED\n")

    # 2. Disk Capacity Check (use C: on Windows, root '/' on POSIX systems)
    target_path = "C:\\" if os.name == "nt" else "/"
    try:
        disk = psutil.disk_usage(target_path)
        free_gigabytes = disk.free // (2**30)
        print_message("info", f"STORAGE ({target_path}): {free_gigabytes}GB FREE\n")
    except OSError as disk_error:
        print_message("error", f"STORAGE CHECK FAILED: {disk_error}\n")


def check_network_speed():
    """Run a download, upload, and ping check using speedtest-cli if installed."""
    print_ascii_banner("INITIATING NETWORK SPEED TEST")

    # Import speedtest in its own block so a missing module returns cleanly without NameError
    try:
        import speedtest
    except (ImportError, ModuleNotFoundError, OSError) as import_error:
        print_message("error", f"SPEEDTEST MODULE MISSING: {import_error}")
        print_message("warning", "Install with: pip install speedtest-cli\n")
        return

    try:
        speedtest_client = speedtest.Speedtest()
        print_message("info", "LOCATING OPTIMAL SERVER...")
        server = speedtest_client.get_best_server()
        server_label = f"{server.get('sponsor', 'Unknown')} ({server.get('name', 'N/A')})"
        print_message("success", f"SERVER: {server_label}\n")

        print_message("info", "TESTING DOWNLOAD SPEED...")
        # Convert bits per second to megabits per second (Mbps)
        download_megabits = speedtest_client.download() / 1_000_000
        print_message("success", f"DOWNLOAD: {download_megabits:.2f} Mbps\n")

        print_message("info", "TESTING UPLOAD SPEED...")
        upload_megabits = speedtest_client.upload() / 1_000_000
        print_message("success", f"UPLOAD: {upload_megabits:.2f} Mbps\n")

        print_message("info", "Pinging the Server")
        ping_milliseconds = speedtest_client.results.ping
        print_message("success", f"PING: {ping_milliseconds} ms\n")
    except (speedtest.SpeedtestException, requests.RequestException) as net_error:
        print_message("error", f"SPEED TEST UPLINK FAILED: {net_error}\n")
    except OSError as os_error:
        print_message("error", f"SPEED TEST OS ERROR: {os_error}\n")
# endregion


# region --- main Process ---
def main():
    """Run the Legion Prime diagnostic and maintenance sequence."""
    # Clear the terminal screen across Windows and POSIX terminals
    os.system("cls" if os.name == "nt" else "clear")

    if os.name == "nt":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            # Enable ENABLE_VIRTUAL_TERMINAL_PROCESSING (0x0004) on stdout (-11)
            handle = kernel32.GetStdHandle(-11)
            mode = ctypes.c_ulong()
            if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                kernel32.SetConsoleMode(handle, mode.value | 0x0004)
        except (AttributeError, OSError):
            pass

    logo = r"""
  _      _____   ____    ___    ___    _   _
 | |    | ____| / ___|  |_ _|  / _ \  | \ | |
 | |    |  _|  | |  _    | |  | | | | |  \| |
 | |___ | |___ | |_| |   | |  | |_| | | |\  |
 |_____||_____| \____|  |___|  \___/  |_| \_|
  \____\ \____\  \____\ \____\ \____\  \_____\
    """
    print_color(logo)
    print_color("           -- LEGION PRIME v1.1 | OMEGAZYPH --")

    get_briefing()
    check_hardware_health()
    run_optimizer()
    check_network_speed()

    print_ascii_ending("LEGION PRIME SEQUENCE COMPLETE.")

    # Pause at the end so output stays readable when launched directly
    try:
        input("\nPress ENTER to return to workstation...")
    except EOFError:
        pass
# endregion


if __name__ == "__main__":
    main()
    