# 🛡️ Wayne's Sentinel Loop: Crypto Trading Bot

A high-performance, automated cryptocurrency trading bot designed for the **Crypto.com** exchange. This bot utilizes **Bollinger Bands** for market entry and exit, featuring a real-time monitoring dashboard and a flexible JSON configuration system.

---

## 🚀 Overview

The Sentinel Loop is a Python-based trading engine that monitors multiple cryptocurrency pairs simultaneously. It uses a 1-hour timeframe to calculate technical indicators and executes trades based on price wicks touching the upper and lower Bollinger Bands.

### Key Features

* **Multi-Pair Monitoring:** Track BTC, ETH, SOL, CRO, and more in a single loop.
* **Real-Time Dashboard:** High-contrast, hacker-style terminal output for live status tracking.
* **State Management:** Persistent logging to CSV ensures the bot remembers its position (WAITING vs. HOLDING) even after a restart.
* **Optimized Polling:** Configurable 15-second check intervals to catch rapid market movements without hitting API rate limits.
* **Safety First:** Built-in insufficient funds handling and buy-state locking to prevent accidental "spam" buying.

---

### 🛠️ Technical Stack

* **Language:** Python 3.x
* **Libraries:** `ccxt` (Exchange API), `pandas` (Data Math), `colorama` (Dashboard Styling).
* **Environment:** Developed on **Windows 11 (WSL2/Ubuntu)** and optimized for home server deployment.
* **IDE:** VSCode.

---

### 📂 Project Structure

SentinelBot/
├── main.py                # Core trading engine and loop logic
├── config.json            # Centralized settings (API keys, pairs, timing)
├── live_trade_log.csv     # Persistent trade history and state tracking
└── README.md              # Project documentation

### ⚙️ Configuration

The bot is controlled via config.json. This allows for live updates to trading parameters without refactoring the core logic.
JSON

{
    "global_settings": {
        "_note_timing": "15 seconds is the sweet spot for stability",
        "check_interval_seconds": 15,
        "trade_dollar_amount": 2.0,
        "base_currency": "USD"
    },
    "trading_pairs": [
        { "symbol": "CRO/USD", "enabled": true, "description": "Cronos" }
    ]
}

### 🚦 Getting Started

1. Prerequisites

    Python 3.10+

    Crypto.com API Key and Secret (with trading permissions enabled).

2. Installation
Bash

### Clone the repository

git clone [https://github.com/your-username/sentinel-loop.git](https://github.com/your-username/sentinel-loop.git)

### Install dependencies

pip install ccxt pandas colorama

3.Running the Bot

To run the bot as a background service on Linux:
Bash

sudo systemctl start cryptobot.service

To monitor live logs using the custom alias:
Bash

### Alias defined in .bashrc

alias bot='journalctl -u cryptobot.service -f -n 30 -q --output cat | grep -v "TERM"'

👤 Author

    Name: Wayne Randall Stock

    Handle: omegazyph

    Status: Intermediate Python & Bash Developer

### 📜 License

This project is for educational and personal use. Trading cryptocurrency involves significant risk.
