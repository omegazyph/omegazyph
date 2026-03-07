# 🚀 Wayne's Crypto Automator

**Author:** omegazyph  
**Last Updated:** 2026-03-07  
**Platform:** Ubuntu Server (SSH access from Lenovo Legion)

## 📌 Project Overview

A Python-based trading simulation using the **15% Drop Re-Buy** strategy. The bot monitors live market data via the Kraken API and maintains a virtual wallet of $20.00.

### 🛠 Tech Stack

* **Language:** Python 3.10+
* **Libraries:** `ccxt`, `colorama`, `python-dotenv`
* **Process Manager:** `systemd` (runs as a background service)
* **Editor:** VSCode (Remote SSH)

---

## 📂 File Structure

text
CryptoAutomator/
├── config.json           # Trading pairs and thresholds
├── trading_log.csv       # Persistent trade history & wallet state
├── .env                  # Environment variables (API keys)
├── RESTART_NOTES.txt     # Quick command cheat sheet
└── scripts/
    ├── main_bot_loop.py  # Main execution engine
    └── market_audit.py   # Secondary log checker

## ⚙️ Management Commands

Start/Stop Service
Action      Command
Start Bot   sudo systemctl start cryptobot
Stop Bot    sudo systemctl stop cryptobot
Restart     sudo systemctl restart cryptobot
Status      sudo systemctl status cryptobot
The Dashboard

To view the live, multi-colored trading terminal, use the custom bash alias:
Bash

bot

## 📈 Trading Logic (15/15 Strategy)

    Initial Entry: Buys $2.00 of a coin when it hits the buy_threshold.

    Safety Nets: If the price drops 15% from the last buy, it re-buys ($2.00), up to 3 times total.

    Exit Strategy: Sells the entire position once the average cost hits a 15% profit target.

    Persistence: All trades are saved to trading_log.csv. On restart, the bot resumes exactly where it left off.

## ⚠️ Important Notes

    API: Uses Kraken for US-compatible data fetching.

    Colors: Uses init(strip=False) in Python and --output cat in the bot alias to ensure colors work over SSH.

    Watchdog: System health is monitored via the external Watchdog service.
    