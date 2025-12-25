Write-Host "--- Starting Maintenance ---" -ForegroundColor Cyan

# 1. CLEANING (Fixed Typos)
Write-Host "[1/4] Cleaning temporary files..." -ForegroundColor Yellow
Remove-Item -Path "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
Clear-RecycleBin -Confirm:$false -ErrorAction SilentlyContinue

# 2. UPDATING (Added --force for Miniconda)
Write-Host "[2/4] Updating all apps..." -ForegroundColor Yellow
winget upgrade --all --accept-package-agreements --accept-source-agreements

# 3. WINDOWS UPDATE
Write-Host "[3/4] Triggering Windows OS Update check..." -ForegroundColor Yellow
control update

# 4. REPAIR
Write-Host "[4/4] Final system health check..." -ForegroundColor Yellow
if ([bool](([System.Security.Principal.WindowsIdentity]::GetCurrent()).Groups -match 'S-1-5-32-544')) {
    sfc /scannow
} else {
    Write-Host "Skipping SFC: Please run this script as ADMINISTRATOR to repair system files." -ForegroundColor Red
}

Write-Host "--- Maintenance Complete! ---" -ForegroundColor Green
Pause