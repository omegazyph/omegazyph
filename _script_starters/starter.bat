@echo off
REM ===============================================================================
REM Project Folder Structure:
REM   Starter-Batch-Project/
REM     └── starter.bat
REM
REM Date:         2026-11-23
REM Script Name:  starter.bat
REM Author:       omegazyph
REM Updated:      2026-11-23
REM Description:  Starter Windows batch script template with directory anchoring,
REM               optional Administrator privilege check, and clean exit handling.
REM ===============================================================================

setlocal EnableExtensions

REM Anchor execution to the directory containing this batch script
cd /d "%~dp0"
if %errorlevel% neq 0 (
    echo [ERROR] Unable to change directory to "%~dp0".
    pause
    exit /b 1
)

echo [INFO] Starting batch script in "%~dp0"...

REM Optional: Check for Administrator privileges using "net session"
net session >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Administrator privileges detected.
) else (
    echo [INFO] Running in standard user mode.
)

REM Place your commands or script calls below this section
echo [SUCCESS] Starter template initialized cleanly.

echo.
pause
endlocal
exit /b 0