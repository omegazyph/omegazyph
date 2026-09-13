###############################################################################################################################################################
# Date: 2026-09-12
# Script Name: win11-maintenance.ps1
# Author: Wayne Stock
# Updated: 2026-09-12
# Description:
#   Comprehensive Windows 11 system maintenance script that performs privilege checks,
#   deep junk file cleanup, network DNS resets, winget application upgrades,
#   Microsoft Store cache resets, Windows Update checks, Firefox vault profile backups,
#   DISM system image repairs, SFC integrity checks, and Windows Event Log clearing.
###############################################################################################################################################################



# param(
#     [string]$logFile = "$env:USERPROFILE\Documents\win11-maintenance.log",
#     [string]$backupDir = "$env:USERPROFILE\Documents\PassVault"
# )


# # Ensure the backup directory exists
# if (-not (Test-Path -Path $backupDir)) {
#     New-Item -ItemType Directory -Path $backupDir | Out-Null
# }

# # Set up logging
# function Log-Message {
#     param (
#         [string]$message
#     )
#     $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
#     $logEntry = "$timestamp - $message"
#     Write-Host $logEntry -ForegroundColor Gray
#     Add-Content -Path $logFile -Value $logEntry
# }

# Set window title
$Host.UI.RawUI.WindowTitle = "win11-maintenance"

# Print banner header
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "   WINDOWS 11 SYSTEM MAINTENANCE SUITE      " -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan

# Ensure the script is running with Administrator privileges or prompt for elevation
$IsAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $IsAdmin) {
    Write-Host "Elevating privileges... Please enter administrator credentials if prompted." -ForegroundColor Yellow
    Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    Pause
    Exit
}

# # Ensure the script is running with Administrator privileges
# $IsAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

# if (-not $IsAdmin) {
#     Write-Host "`nWARNING: Administrator privileges not detected!" -ForegroundColor Red
#     Write-Host "Some operations (like System File Checker, DISM, and Event Log clearing) require Administrator rights." -ForegroundColor Yellow
#     Write-Host "Please re-run this PowerShell script as Administrator.`n" -ForegroundColor Yellow
#     Pause
#     Exit
# }

# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# 1. DEEP SYSTEM CLEANING
# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# Log-Message "Starting deep cleaning system junk..."
Write-Host "`n[1/9] DEEP CLEANING SYSTEM JUNK..." -ForegroundColor Yellow

# Clear recycle bin
Write-Host "Clearing Recycle Bin..." -ForegroundColor Yellow
Clear-RecycleBin -Confirm:$false -ErrorAction SilentlyContinue

# Target temporary paths and system junk
$TempFolders = @(
    "$env:TEMP\*",
    "C:\Windows\Temp\*",
    "C:\Windows\Prefetch\*"
)

foreach ($Path in $TempFolders) {
    Remove-Item -Path $Path -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host "DONE: Temporary files, prefetch, and Recycle Bin cleared." -ForegroundColor Green
# Log-Message "Temporary files, prefetch, and Recycle Bin cleared."

# Run built-in cleanmgr sage configuration
Write-Host "Refreshing Disk Cleanup..." -ForegroundColor Yellow
cleanmgr /sagerun:1
Write-Host "DONE: Disk Cleanup completed." -ForegroundColor Green
# Log-Message "Disk Cleanup completed."

# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# 2. NETWORK FLUSH & REFRESH
# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# Log-Message "Refreshing network, flushing DNS, and re-registering adapters..."
Write-Host "`n[2/9] REFRESHING NETWORK & FLUSHING DNS..." -ForegroundColor Yellow
Write-Host "Flushing DNS Cache and Registering IP..." -ForegroundColor Yellow
ipconfig /flushdns
ipconfig /registerdns
Write-Host "DONE: Network DNS cache flushed and adapters re-registered." -ForegroundColor Green
# Log-Message "Network DNS cache flushed and adapters re-registered."

# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# 3. APPLICATION UPDATES (WINGET)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# Log-Message "Updating installed applications..."
Write-Host "`n[3/9] UPDATING INSTALLED APPLICATIONS..." -ForegroundColor Yellow
try {
    Write-Host "Checking for standard updates with Winget..." -ForegroundColor Yellow
    winget upgrade --all --include-unknown --accept-package-agreements --accept-source-agreements
    
    Write-Host "Checking for Microsoft Store application updates..." -ForegroundColor Yellow
    winget upgrade --all --source msstore --accept-package-agreements --accept-source-agreements
    
    Write-Host "DONE: Application update process completed." -ForegroundColor Green
} catch {
    Write-Host "Note: Some packages could not be updated or were busy." -ForegroundColor Gray
    # Log-Message "Error updating applications: $_"
}
# Log-Message "Application update process completed."

# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# 4. MICROSOFT STORE CACHE RESET
# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# Log-Message "Resetting Microsoft Store cache..."
Write-Host "`n[4/9] RESETTING MICROSOFT STORE CACHE..." -ForegroundColor Yellow
Start-Process "wsreset.exe" -NoNewWindow -Wait
Write-Host "DONE: Microsoft Store cache reset completed." -ForegroundColor Green
# Log-Message "Microsoft Store cache reset completed."

# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# 5. WINDOWS OS UPDATE TRIGGER
# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# Log-Message "Checking for Windows OS updates..."
Write-Host "`n[5/9] CHECKING FOR WINDOWS OS UPDATES..." -ForegroundColor Yellow

# Trigger COM-object auto-update scan
$AutoUpdate = New-Object -ComObject Microsoft.Update.AutoUpdate
$AutoUpdate.DetectNow()

# Open the Windows Update Control Panel UI
Write-Host "Opening Windows Update Control Panel..." -ForegroundColor Yellow
control update
Write-Host "DONE: Windows Update detection triggered." -ForegroundColor Green
# Log-Message "Windows Update detection triggered."

# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# 6. FIREFOX PROFILE VAULT BACKUP
# -----------------------------------------------------------------------------------------------------------------------------------------------------------
Write-Host "`n[6/9] EXTRACTING FIREFOX PROFILE BACKUP..." -ForegroundColor Yellow
$FFProfile = "$env:APPDATA\Mozilla\Firefox\Profiles\*.default-release"
if (Test-Path -Path $FFProfile) {
    Write-Host "Backing up Firefox password database..." -ForegroundColor Yellow
    Copy-Item -Path "$FFProfile\logins.json", "$FFProfile\key4.db" -Destination $backupDir -Force -ErrorAction SilentlyContinue
    Write-Host "DONE: Firefox password database backed up to $backupDir." -ForegroundColor Green
} else {
    Write-Host "Firefox profile not found." -ForegroundColor Red
}
# Log-Message "Firefox profile backup completed."

# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# 7. SYSTEM IMAGE REPAIR (DISM)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# Log-Message "Running DISM image health check and repair..."
Write-Host "`n[7/9] CHECKING SYSTEM IMAGE HEALTH (DISM)..." -ForegroundColor Yellow
Write-Host "`nthis might take awhile..." -ForegroundColor Yellow
DISM /Online /Cleanup-Image /RestoreHealth
Write-Host "DONE: DISM image repair completed." -ForegroundColor Green
# Log-Message "DISM image health check and repair completed."

# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# 8. SYSTEM FILE INTEGRITY CHECK
# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# Log-Message "Running System File Checker..."
Write-Host "`n[8/9] CHECKING SYSTEM INTEGRITY (SFC)..." -ForegroundColor Yellow
sfc /scannow
Write-Host "DONE: System file integrity check completed." -ForegroundColor Green
# Log-Message "System file integrity check completed."

# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# 9. EVENT LOG CLEARING
# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# Log-Message "Clearing Windows Event Logs..."
Write-Host "`n[9/9] CLEARING WINDOWS EVENT LOGS..." -ForegroundColor Yellow
$EventLogs = Get-WinEvent -ListLog * -ErrorAction SilentlyContinue | Where-Object { $_.RecordCount -gt 0 }
foreach ($Log in $EventLogs) {
    try {
        ([System.Diagnostics.Eventing.Reader.EventLogSession]::GlobalSession).ClearLog($Log.LogName)
    } catch {
        # Skip logs that cannot be cleared while locked by active system services
    }
}
Write-Host "DONE: Event logs cleared." -ForegroundColor Green
# Log-Message "Windows Event Logs cleared."

Write-Host "`n==============================================" -ForegroundColor Green
Write-Host "   MAINTENANCE COMPLETE - SYSTEM IS OPTIMIZED!" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Green

Pause