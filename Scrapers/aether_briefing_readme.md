# Aether Briefing (`aether_briefing.py`)

A lightweight, terminal-based daily briefing utility written in Python. `aether_briefing.py` clears your console, displays a custom ANSI-styled ASCII header, and fetches live top tech headlines alongside automatic IP-based local weather conditions.

---

## Features

- **Typewriter ANSI Terminal UI:** Character-by-character animated output (`print_color`) paired with a 24-bit RGB and bold ANSI color palette.
- **Unified Semantic Messaging:** Categorized console output (`print_message`) with distinct tags and colors:
  - `[~]` **Status** (24-bit Magenta) — Active network probes and progress updates
  - `[*]` **Info** (Bold Blue) — Retrieved headlines and weather details
  - `[+]` **Success** (Bold Green) — Completed operations
  - `[!]` **Warning** (Bold Yellow) — Non-critical alerts
  - `[X]` **Error** (Bold Red) — Uplink, HTTP, or parsing failures
- **Live Tech Headlines:** Fetches the top 5 current stories from the official Hacker News Firebase API.
- **Automatic Local Weather:** Queries `wttr.in` using IP-based geolocation to display current weather and wind conditions without manual city configuration.
- **Resilient Network Handling:** Enforces 10-second timeouts (`timeout=10`), HTTP status validation (`raise_for_status()`), and targeted exception handling (`requests.RequestException`) so stalled endpoints never freeze your terminal.

---

## Project Structure

```text
project_root/
├── aether_briefing.py
└── aether_briefing_readme.md
```

---

## Prerequisites

- **Python:** Python 3.7 or higher
- **Terminal:** Any modern terminal emulator supporting ANSI escape sequences and 24-bit TrueColor (e.g., Windows Terminal, iTerm2, GNOME Terminal, Alacritty, Kitty)
- **Dependencies:** `requests`

---

## Installation

1. **Clone or download** `aether_briefing.py` into your project directory.
2. **Install the required third-party library:**

```bash
pip install requests
```

---

## Usage

Run the script directly from your terminal:

```bash
python aether_briefing.py
```

### What It Does on Execution

1. Clears the terminal screen (`cls` on Windows, `clear` on Unix/macOS).
2. Prints the framed `AETHER` banner along with connection status and the current local timestamp.
3. Connects to Hacker News and prints the top 5 tech headlines.
4. Scans your IP geolocation via `wttr.in` and prints your current local weather summary.
5. Displays a closing banner signaling that your environment is ready.

---

## Customization

- **Typing Speed:** Adjust `time.sleep(0.01)` inside `print_color()` to speed up or slow down the typewriter animation.
- **Headline Count:** Change the slice `[:5]` in `get_tech_news()` to display more or fewer Hacker News stories.
- **Request Timeouts:** Modify `timeout=10` in `get_tech_news()` and `get_universal_weather()` to tighten or relax network wait times.
- **Color Palette:** Edit the ANSI constants at the top of `aether_briefing.py` (`BLUE`, `MAGENTA`, `PURPLE`, `RED`, `GREEN`, `YELLOW`, `CYAN`) to match your terminal theme.

---

## Author

- **Omegazyph** — *Created: 2026-01-07 | Updated: 2026-11-23*
