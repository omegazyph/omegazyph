# Trucking Mileage & Expense Tracker

**Author:** omegazyph  
**Started:** 2026-01-15  
**Last Updated:** 2026-01-15

## 🚛 Project Overview

A modular Python/Tkinter application designed to track trucking trip data, calculate fuel efficiency (MPG), and determine total cost-per-mile (CPM). The app uses a permanent JSON dictionary to store recurring fixed costs (insurance, permits, etc.) so they persist across sessions.

## 📂 File Structure

- `scripts/main.py`: The primary calculator GUI.
- `scripts/settings.py`: The management tool for editing fixed costs.
- `data/expenses.json`: Permanent storage for recurring expenses.
- `data/trips/`: Directory containing individual Trip Report text files.

## 🛠 Features Completed

- [x] **Modular Design:** Logic split between calculation and settings.
- [x] **Persistence:** Fixed costs saved in JSON format.
- [x] **GUI Interface:** Clean Tkinter layout on Windows 11.
- [x] **Keyboard Shortcut:** 'Enter' key bound to calculate function.
- [x] **Individual Reporting:** Saves human-readable `.txt` files named by Trip Number.
- [x] **Dynamic Footer:** Shows the current total of fixed expenses on the main screen.

## 📝 Planned Mods (To-Do)

- [ ] **Income Tracking:** Add a field for "Gross Income" to calculate net profit per trip.
- [ ] **History Viewer:** Create a button to browse and open past Trip Reports.
- [ ] **Odometer Automation:** Automatically pull the ending mileage of the last trip as the starting mileage of the new trip.
- [ ] **Summary Statistics:** A tool to calculate totals for the week/month.

## 🚀 How to Run

1. Open the project folder in **VSCode**.
2. Ensure you have Python installed.
3. Run `python scripts/main.py` from the terminal.
