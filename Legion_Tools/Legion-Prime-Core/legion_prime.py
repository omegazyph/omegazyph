###############################################################################
# Date: 2026-01-07
# Script Name: legion_prime.py
# Author: omegazyph
# Updated: 2026-01-07
# Description: The "God-Mode" suite. Combines System Optimization, 
#              Location-Aware Weather, Tech News, and Network Probing.
###############################################################################

import os
import sys
import time
import requests
import psutil
import subprocess


def print_color(text, color="\033[1;32m"):
    """Matrix-style typing effect."""
    reset = "\033[0m"
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.008)
    print(reset)

def get_briefing():
    print_color("\n" + "="*54)
    print_color(" [!] INITIATING PROJECT AETHER: GLOBAL UPLINK")
    print_color("="*54)
    
    # 1. Universal Weather (Auto-Location)
    try:
        weather = requests.get("https://wttr.in/?format=4", timeout=5).text.strip()
        print_color(f"[>] ENV: {weather}", "\033[1;36m")
    except Exception:
        print_color("[-] WEATHER UPLINK OFFLINE", "\033[1;31m")

    # 2. Tech News
    try:
        news_ids = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=5).json()[:3]
        print_color("\n--- LATEST INTELLIGENCE ---")
        for n_id in news_ids:
            story = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{n_id}.json").json()
            print(f"\033[1;32m [>] {story['title']}\033[0m")
    except Exception:
        print_color("[-] NEWS UPLINK OFFLINE", "\033[1;31m")

def run_optimizer():
    print_color("\n" + "="*54)
    print_color(" [!] INITIATING LEGION OPTIMIZER: SYSTEM PURGE")
    print_color("="*54)
    
    # SSD Trim (Needs Admin)
    print_color("[*] OPTIMIZING SSD STORAGE...")
    subprocess.run(["defrag", "C:", "/O"], capture_output=True)
    
    # DNS Flush
    print_color("[*] FLUSHING NETWORK CACHE...")
    subprocess.run(["ipconfig", "/flushdns"], capture_output=True)
    
    # RAM Check
    mem = psutil.virtual_memory()
    print_color(f"[>] RAM STABILITY: {mem.percent}% UTILIZED", "\033[1;36m")

def check_hardware_health():
    print_color("\n" + "="*54)
    print_color(" [!] DIAGNOSING LEGION HARDWARE PULSE")
    print_color("="*54)

    # 1. Battery Health
    battery = psutil.sensors_battery()
    if battery:
        status = "Charging" if battery.power_plugged else "Discharging"
        color = "\033[1;32m" if battery.percent > 20 else "\033[1;31m"
        print_color(f"[>] BATTERY: {battery.percent}% ({status})", color)
    
    # 2. SSD Capacity Check (C: Drive)
    disk = psutil.disk_usage('C:')
    free_gb = disk.free // (2**30) # Convert bytes to GB
    print_color(f"[>] STORAGE: {free_gb}GB REMAINING ON C:", "\033[1;36m")

def check_network_speed():
    """Defines the network speed test module."""
    print_color("\n" + "="*54)
    print_color(" [!] INITIATING NETWORK SPEED TEST")
    print_color("="*54)
    
    try:
        import speedtest
        st = speedtest.Speedtest()
        
        print_color("[*] LOCATING OPTIMAL SERVER...")
        st.get_best_server()
        
        print_color("[*] TESTING DOWNLOAD SPEED...")
        # st.download() returns bits; we divide by 1,000,000 for Mbps
        download_mbit = st.download() / 1000000
        
        print_color("[*] TESTING UPLOAD SPEED...")
        upload_mbit = st.upload() / 1000000
        
        ping = st.results.ping
        
        print_color(f"\n[>] DOWNLOAD: {download_mbit:.2f} Mbps", "\033[1;32m")
        print_color(f"[>] UPLOAD:   {upload_mbit:.2f} Mbps", "\033[1;32m")
        print_color(f"[>] PING:     {ping} ms", "\033[1;36m")
        
    except Exception as e:
        print_color("[-] SPEED TEST UPLINK FAILED: " + str(e), "\033[1;31m")

def main():
    os.system('cls')
    # Using triple quotes r""" ensures Python treats the entire block as text.
    logo = r"""
  ______  __  __  ______  ______  ______  ______  __  __   
 /\  __ \/\ \/\ \/\  ___\/\  ___\/\  __ \/\  ___\/\ \_\ \  
 \ \ \_\ \ \ \_\ \ \  __\\ \ \__ \ \ \_\ \ \  __\\ \____ \ 
  \ \_____\ \_____\ \_____\ \_____\ \_____\ \_____\/\_____\
   \/_____/\/_____/\/_____/\/_____/\/_____/\/_____/\/_____/
    """
    print_color(logo)
    print_color("           -- LEGION PRIME v1.0 | OMEGAZYPH --")
    
    run_optimizer()
    get_briefing()
    check_hardware_health()
    check_network_speed()

    print_color("\n" + "="*54)
    print_color(" [SUCCESS] SYSTEM OPTIMIZED. UPLINK SECURE.")
    print_color("="*54)
    input("\nPress ENTER to return to workstation...")

if __name__ == "__main__":
    main()