# 📊 Employee CSV Directory Reader (v1.3)

## 📝 Overview

Developed by **Wayne Stock (omegazyph)**, this project is a streamlined utility for parsing and displaying employee contact information. Originally created as a Code Academy exercise, it has been refactored into a standalone tool with robust error handling and dynamic file pathing.

## ✨ Key Features

* **Dynamic Path Resolution:** Uses `os.path` to automatically locate the data file within its own directory, making the project fully portable.
* **Specialized Parsing:** Configured with a custom `quotechar` to cleanly handle single-quoted data values (e.g., `'Name'`).
* **Table Formatting:** Utilizes f-string padding to generate a perfectly aligned directory in the terminal.
* **Safe Data Access:** Employs the `.get()` method to prevent script crashes if a specific data field is missing from a row.

## 📂 Project Structure

text
Employee_CSV_Project/
├── CSV_reading.py    # Main execution script
└── employees.csv     # Data source (Single-quote format)

## 🚀 Getting Started

    Ensure Python is installed.

    Navigate to the project folder:
    Bash

cd Employee_CSV_Project

Run the script:
Bash

    python3 CSV_reading.py

## 🛠️ Data Format

The script is designed to read a CSV structured with single quotes and the following headers: 'Name', 'Email', 'Phone Number'

Author: Wayne Stock (omegazyph)

Version: 1.3

Last Updated: 2026-01-05
