# 🛠️ Legion System Optimizer (Stable v2.1)

A high-performance maintenance utility specifically tuned for the **Lenovo Legion** running Windows 11 Home. This tool combines real-time hardware diagnostics with system-level optimization protocols.

---

## ⚡ Core Functions

* **SSD Optimization (TRIM):** Triggers the Windows `defrag /O` command to maintain high write speeds on the internal NVMe SSD and LaCie (Z:) drive.
* **Network Flush:** Clears the DNS cache to resolve latency issues and refresh connectivity.
* **Memory Probe:** Monitors real-time RAM availability and power status using the `psutil` sensor suite.
* **Storage Cleanup:** Purges temporary system files to reclaim space and remove cached "junk" data.

---

## ⚙️ Installation

### 1. Requirements

This script requires the `psutil` library to read your Legion's hardware sensors:

bash
pip install psutil

2.Administrator Access

Crucial: Because this script manages disk hardware and network caches, it must be run in a Terminal with Administrator Privileges.

## 🚀 How to Run

    Open Windows Terminal (Run as Administrator).

    Navigate to your script directory.

    Execute the protocol:

Bash

python legion_optimizer_fixed.py

Visual Experience

Optimized for the OmegaZyph Hacker Station:

    Color: Matrix Green (#00FF41)

    Effect: Retro Scanlines & Glow enabled.

    Transparency: 70% Acrylic.

## 📂 System Impact

Task Operation Benefit
Disk defrag /O Extends SSD lifespan & maintains speed.
Network ipconfig /flushdnsn Reduces "Server Not Found" errors.
Cleanup del %TEMP%n Frees up space on C: Drive.

## 📜 Metadata

    Author: omegazyph

    Hardware Target: Lenovo Legion

    OS Target: Windows 11 Home

    Updated: 2026-01-07

---

### Pro Tip for your VS Code Setup:

You can keep this `README.md` open in a split window in VS Code while you edit your Python code. To see the professional formatting, click the **"Open Preview to the Side"** icon (it looks like a small page with a magnifying glass) in the top right corner of VS Code.
