# 📊 Employee Data Processor

## **Automated CSV Parsing and Contact Extraction**

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![Environment](https://img.shields.io/badge/platform-Windows%2011%20Home-lightgrey.svg)
![Author](https://img.shields.io/badge/author-omegazyph-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Overview

A robust Python-based utility developed for the **Exam Coding** module. This tool streamlines the process of reading flat-file databases (`.csv`) and converting raw data into a human-readable contact directory. It leverages the `DictReader` class for high-reliability field mapping.

---

## ⚙️ Technical Features

* **Path Integrity:** Utilizes `os` module for path verification to prevent runtime exceptions.
* **Safe Data Retrieval:** Implements `.get()` method to handle missing fields without breaking the loop.
* **Buffer Management:** Uses the `newline=''` parameter in `open()` for cross-platform CSV compatibility.
* **Visual Alignment:** Employs `.ljust()` string padding for professional terminal formatting.

---

## 📂 System Requirements

| Requirement | Specification |
| :--- | :--- |
| **OS** | Windows 11 Home (Lenovo Legion optimized) |
| **Language** | Python 3.8 or higher |
| **Data Format** | RFC 4180 compliant CSV |
| **IDE** | Visual Studio Code |

---

## 🚀 Execution Profile

To initialize the script, navigate to your project directory in the terminal and execute:

```bash
python employee_lookup.py

Input Data Schema

Ensure your employees.csv follows this structure:
Code snippet

Name,Phone Number,Department
John Doe,555-0101,IT
Jane Smith,555-0102,Marketing

🛠 Project Structure
Plaintext

Exam_coding/
├── CSV_reading/
│   ├── employees.csv        # Database Source
│   └── employee_lookup.py   # Main Logic
└── README.md                # Documentation

⚖️ License

This project is licensed under the MIT License.

Permitted:

    ✅ Commercial use

    ✅ Modification

    ✅ Distribution

    ✅ Private use

Conditions:

    ℹ️ Must include the original copyright notice and this permission notice in all copies or substantial portions of the software.

Copyright (c) 2026 omegazyph
