###############################################################################
# Date: 2026-01-07
# Script Name: aether_briefing.py
# Author: omegazyph
# Updated: 2026-01-07
# Description: Scrapes tech headlines and weather to provide a daily 
#              terminal briefing.
###############################################################################

import requests
import time
import sys

def print_hacker(text, color="\033[1;32m"):
    """Matrix-style typing effect."""
    reset = "\033[0m"
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)
    print(reset)

def get_tech_news():
    print_hacker("[!] PROBING HACKER NEWS UPLINK...")
    try:
        # Using a simple API version of Hacker News for stability
        response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
        top_ids = response.json()[:5]  # Get top 5 stories
        
        print_hacker("\n--- TOP TECH HEADLINES ---")
        for item_id in top_ids:
            item = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json").json()
            print(f"\033[1;36m[>] {item['title']}\033[0m")
            time.sleep(0.2)
    except Exception:
        print_hacker("[!] NEWS UPLINK FAILED", "\033[1;31m")

def get_universal_weather():
    # No city specified = Auto-location based on your IP
    print_hacker("\n[!] SCANNING LOCAL GEOLOCATION...")
    try:
        # format=4 includes city name, weather, and wind speed
        response = requests.get("https://wttr.in/?format=4")
        if response.status_code == 200:
            weather_data = response.text.strip()
            print_hacker(f"[>] LOCATION ESTABLISHED: {weather_data}", "\033[1;36m")
        else:
            print_hacker("[!] WEATHER SERVER UNREACHABLE", "\033[1;31m")
    except Exception:
        print_hacker("[!] UPLINK ERROR: CHECK INTERNET CONNECTION", "\033[1;31m")

def run_aether():
    print_hacker("======================================================")
    print_hacker("     _______  _______ _________          _______      ")
    print_hacker(r"    (  ___  )(  ____ \\__   __/|      /|(  ____ \     ")
    print_hacker(r"    | (   ) || (    \/   ) (   | )   ( || (    \/     ")
    print_hacker("    | |___| || (__       | |   | (___) || (__         ")
    print_hacker("    |  ___  ||  __)      | |   |  ___  ||  __)        ")
    print_hacker("    | (   ) || (         | |   | (   ) || (           ")
    print_hacker(r"    | )   ( || (____/\   | |   | )   ( || (____/\     ")
    print_hacker(r"    |/     \|(_______/   )_(   |/     \|(_______/     ")
    print_hacker("======================================================")
    print_hacker(" STATUS: SECURE CONNECTION ESTABLISHED")
    print_hacker(f" DATE:   {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print_hacker("======================================================\n")

    get_tech_news()
    get_universal_weather()

    print_hacker("\n======================================================")
    print_hacker("   BRIEFING COMPLETE. SYSTEM READY FOR CODING.        ")
    print_hacker("======================================================")

if __name__ == "__main__":
    run_aether()