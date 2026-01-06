# 🃏 OMEGAZYPH Blackjack (v2.5)

## 📝 Overview

**OMEGAZYPH Blackjack** is a terminal-based implementation of the classic casino game. Built with Python, this version features a persistent bankroll system, high-score tracking, and a dynamic ASCII-based card rendering engine. The game follows standard house rules where the dealer must stand on 17.

## ✨ Key Features

* **Dynamic ASCII Art:** Cards are rendered side-by-side in the terminal for an immersive visual experience.
* **Persistent Bankroll:** Your balance carries over from round to round until you choose to quit or go bust.
* **High-Score Tracking:** Achieving a new peak balance automatically updates the `high_score.txt` file.
* **Smart Ace Logic:** The scoring engine automatically adjusts Ace values (1 or 11) to prevent the player from busting whenever possible.
* **Defensive Programming:** Includes robust input validation to handle non-numeric bets or invalid menu choices.

## 📂 System Architecture

| File | Type | Description |
| :--- | :--- | :--- |
| **`blackjack_pro.py`** | Script | The main game engine and UI logic. |
| **`high_score.txt`** | Data | A persistent file that stores the `Name:Score` of the top player. |

## 🚀 Getting Started

### 🔧 Prerequisites

* **Python 3.x** installed on your system.
* A terminal that supports **UTF-8 characters** (to display the ♥, ♦, ♣, ♠ suit symbols).

### 🏃 Running the Game

1. Navigate to the directory containing the script.
2. Execute the script using Python:

bash
python3 blackjack_pro.py

## 📋 Game Rules

    Goal: Beat the dealer's hand without exceeding 21.

    Dealer Rules: The dealer must hit until their total is at least 17.

    Payouts: Winning a hand pays out 2:1 (your bet back plus the winnings).

    Push: If the scores are equal, your bet is returned to your balance.

Developer: omegazyph

Version: 2.5 (Lint-Free Edition)

Date Updated: January 5, 2026
