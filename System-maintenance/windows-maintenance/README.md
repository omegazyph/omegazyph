# Windows 11 System Maintenance Suite 🛡️

**Author:** Omegazyph  
**Date:** September 12, 2026  
**Version:** v1.0.0  
**Platform:** Windows 11 (PowerShell)  

## 📖 Description

`win11-maintenance.ps1` is a comprehensive, automated system maintenance utility written in PowerShell. It is designed to perform routine deep cleaning, network diagnostics, package upgrades, security backups, and core system integrity repairs on Windows 11 environments.

The script incorporates an automatic privilege elevation check to ensure administrative commands execute successfully.

## 🚀 Key Features & Workflow

The script executes a 9-step automated maintenance routine:

1. **Deep System Junk Cleaning:**
   * Clears the Windows Recycle Bin without confirmation prompts.
   * Purges temporary files from user temp paths, system temp folders, and prefetch directories.
   * Triggers the built-in Windows Disk Cleanup tool (`cleanmgr`).
2. **Network Flush & Refresh:**
   * Flushes the local DNS resolver cache (`ipconfig /flushdns`) and re-registers network adapters (`ipconfig /registerdns`).
3. **Application Upgrades (Winget):**
   * Automatically scans and updates standard applications and Microsoft Store packages via the Windows Package Manager (`winget`).
4. **Microsoft Store Cache Reset:**
   * Resets the Windows Store cache (`wsreset.exe`) to resolve application launch or download issues.
5. **Windows OS Update Trigger:**
   * Forces a COM-object auto-update detection scan and launches the native Windows Update settings panel.
6. **Firefox Profile Vault Backup:**
   * Automatically extracts and backs up critical credential and profile files (`logins.json` and `key4.db`) to a designated local vault directory (`PassVault`).
7. **System Image Repair (DISM):**
   * Executes Deployment Image Servicing and Management (`DISM /Online /Cleanup-Image /RestoreHealth`) to repair corrupted system images.
8. **System File Integrity Check (SFC):**
   * Runs the System File Checker (`sfc /scannow`) to verify and replace missing or damaged protected operating system files.
9. **Event Log Clearing:**
   * Clears active Windows Event Logs while safely bypassing locked or active system service logs.

---

## 🛠️ Prerequisites & Execution

* **Operating System:** Windows 11
* **Permissions:** Administrator privileges are required. The script features built-in self-elevation logic and will automatically prompt you to accept UAC credentials if launched normally.

### Usage Instructions

1. Open PowerShell as a standard user or administrator.
2. Navigate to the directory containing your script:

   cd "C:\Path\To\Your\ScriptFolder"

3. Execute the script (ensure your execution policy allows local scripts):
    PowerShell

4. Set-ExecutionPolicy Bypass -Scope Process -Force
    .\win11-maintenance.ps1

## 📁 Project Structure

Win11Maintenance/

├── win11-maintenance.ps1      # Main automated

PowerShell utility

└── README.md                  # Project documentation

## 📅 Development History

    v1.0.0: Initial release featuring automated junk removal, network flushing, winget upgrades, Firefox vault backups, DISM/SFC integrity checks, and event log clearing.
---
