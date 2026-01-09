# Check for Admin rights (needed for system updates)
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Please run this script as Administrator!" -ForegroundColor Red
    Pause
    Exit
}

Write-Host "--- Windows 11 Super Maintenance Started ---" -ForegroundColor Cyan

# 1. DEEP CLEANING
Write-Host "`n[1/4] Cleaning System Junk..." -ForegroundColor Yellow
# Empties Recycle Bin, Temp folders, and Old Update leftovers
Clear-RecycleBin -Confirm:$false -ErrorAction SilentlyContinue
Remove-Item -Path "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "C:\Windows\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue

# 2. NETWORK REFRESH (Lower Ping for Gaming)
Write-Host "[2/4] Flushing DNS and Resetting Network..." -ForegroundColor Yellow
ipconfig /flushdns

# 3. APP UPDATES (The 'Winget' Way)
Write-Host "[3/4] Updating all Apps (Winget)..." -ForegroundColor Yellow
winget upgrade --all --include-unknown --accept-package-agreements --accept-source-agreements

# 4. WINDOWS OS UPDATES
Write-Host "[4/4] Checking for Windows OS Updates..." -ForegroundColor Yellow
# This uses the built-in Windows Update trigger
$AutoUpdate = New-Object -ComObject Microsoft.Update.AutoUpdate
$AutoUpdate.DetectNow()

Write-Host "`n--- All Tasks Finished! ---" -ForegroundColor Green
Write-Host "Your PC is clean and updates are processing in the background."
Pause