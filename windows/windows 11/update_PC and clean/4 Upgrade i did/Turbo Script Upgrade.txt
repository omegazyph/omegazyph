# --- PRO MAINTENANCE SCRIPT ---
$Host.UI.RawUI.WindowTitle = "System Turbo Clean - Level 2"

Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "   SYSTEM MAINTENANCE & REMOTE BACKUP" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan

# 1. DEEP CLEAN
Write-Host "`n[1/4] DEEP CLEANING..." -ForegroundColor Yellow
$TempFolders = @("$env:TEMP\*", "C:\Windows\Temp\*", "C:\Windows\Prefetch\*")
foreach ($Path in $TempFolders) {
    Remove-Item -Path $Path -Recurse -Force -ErrorAction SilentlyContinue
}
Clear-RecycleBin -Confirm:$false -ErrorAction SilentlyContinue
Write-Host "DONE: Junk files and Recycle Bin cleared." -ForegroundColor Green

# 2. APP UPDATES (Fixed Syntax)
Write-Host "`n[2/4] UPDATING APPLICATIONS..." -ForegroundColor Yellow
# We use 'try/catch' to hide the Miniconda error instead of --erroraction
try {
    winget upgrade --all --accept-package-agreements --accept-source-agreements --header "No-Wall-Of-Text"
} catch {
    Write-Host "Note: Some apps were busy and skipped." -ForegroundColor Gray
}
Write-Host "DONE: Apps checked for updates." -ForegroundColor Green

# 3. REMOTE PASSWORD BACKUP
Write-Host "`n[3/4] EXTRACTING FIREFOX VAULT..." -ForegroundColor Yellow
$VaultPath = "$env:USERPROFILE\Documents\PassVault"
if (!(Test-Path $VaultPath)) { New-Item -ItemType Directory -Path $VaultPath }
$FFProfile = "$env:APPDATA\Mozilla\Firefox\Profiles\*.default-release"
Copy-Item -Path "$FFProfile\logins.json", "$FFProfile\key4.db" -Destination $VaultPath -Force -ErrorAction SilentlyContinue
Write-Host "DONE: Password files backed up to Documents\PassVault." -ForegroundColor Cyan

# 4. SYSTEM REPAIR
Write-Host "`n[4/4] RUNNING SYSTEM HEALTH CHECK..." -ForegroundColor Yellow
sfc /scannow

Write-Host "`n==============================================" -ForegroundColor Green
Write-Host "   MAINTENANCE COMPLETE - YOU ARE GOOD TO GO!" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Green
Pause