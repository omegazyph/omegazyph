
# 🛰️ Aether Briefing

Aether Briefing is a Python-based terminal utility designed for the **Lenovo Legion** environment. It serves as a digital "morning report," scraping high-level tech intelligence and local environmental data to prepare the user for a day of coding.

## 🚀 Features

* **Matrix Interface:** All output is rendered with a custom "hacker-style" typing effect (`print_hacker`) in neon green.
* **Intelligence Gathering:** Scrapes the top 5 trending stories from the Hacker News API.
* **Geo-Location Weather:** Uses auto-IP detection via `wttr.in` to provide local weather without requiring an API key.
* **Secure Connection:** Real-time timestamping for every briefing session.

---

## 🛠️ Requirements

Since you are using **VS Code** on **Windows 11**, ensure you have the `requests` library installed in your environment:

bash
pip install requests

## 📂 Installation & Usage

    Clone/Copy the aether_briefing.py script into your main tool directory.

    Open your VS Code terminal.

    Run the script using:
    Bash

    python aether_briefing.py

## 🏗️ Technical Architecture

The script is built with three core modules:
Module Function Resource Used
News Uplink get_tech_news() Hacker News Firebase API
Weather Scan get_universal_weather() Wttr.in (CURL-based weather)
Visual Engine print_hacker() Sys.stdout buffer manipulation

## 📝 Author Notes (omegazyph)

This tool was designed to be the first script run upon system boot. It provides immediate context on the global tech landscape and local conditions, allowing for a focused transition into development work.

Warning: Ensure you have an active internet connection, as the script requires external API uplinks to populate data.
