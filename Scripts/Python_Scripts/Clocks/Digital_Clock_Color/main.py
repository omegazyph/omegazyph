# Date: 2026-08-17
# Script Name: main.py
# Author: omegazyph
# Last Updated: 2026-08-17
# Description: Displays a digital clock in the terminal that changes color every second.

import time
from datetime import datetime, timezone

from colorama import Fore, init

# Initialize Colorama with autoreset enabled so color settings do not bleed into subsequent output
init(autoreset=True)

# Define the list of available colors for rotation
COLORS = [
    Fore.RED,
    Fore.GREEN,
    Fore.YELLOW,
    Fore.CYAN,
    Fore.MAGENTA,
    Fore.BLUE,
]

try:
    while True:
        # Get current local time formatted as HH:MM:SS with local timezone awareness
        now = datetime.now(timezone.utc).astimezone().strftime("%H:%M:%S")

        # Select a color based on the current Unix timestamp
        color = COLORS[int(time.time()) % len(COLORS)]

        # Print the colorized timestamp at the beginning of the line
        # flush=True ensures the output is immediately displayed in the terminal window
        print(f"\r{color}{now}", end="", flush=True)

        # Pause execution for one second before the next refresh
        time.sleep(1)

except KeyboardInterrupt:
    # Gracefully print a new line upon script cancellation (Control + C) so terminal prompt appears cleanly below
    print()