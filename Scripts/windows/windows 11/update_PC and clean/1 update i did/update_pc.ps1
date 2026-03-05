Write-Host "--- Starting Kali-style Windows Update ---" -ForegroundColor Cyan

# 1. Update all Windows Apps via Winget
Write-Host "[1/3] Updating all applications..." -ForegroundColor Yellow
winget upgrade --all --include-unknown --accept-package-agreements --accept-source-agreements

# 2. Windows System Update (Optional - requires PSWindowsUpdate module)
Write-Host "[2/3] Cleaning temporary files and system junk..." -ForegroundColor Yellow
cleanmgr /sagerun:1

# 3. System File Check (Repairing OS health)
Write-Host "[3/3] Checking system integrity..." -ForegroundColor Yellow
sfc /scannow

Write-Host "--- Maintenance Complete! ---" -ForegroundColor Green
Pause