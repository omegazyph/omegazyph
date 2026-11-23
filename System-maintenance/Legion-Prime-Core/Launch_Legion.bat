@echo off
REM ===============================================================================
REM Project Folder Structure:
REM   Legion-Prime-Core/
REM     ├── README.md
REM     ├── launch_legion.bat
REM     └── legion_prime.py
REM
REM Date:         2026-01-07
REM Script Name:  launch_legion.bat
REM Author:       omegazyph
REM Updated:      2026-11-23
REM Description:  Checks for Administrator privileges on Windows, requests
REM               elevation via native ShellExecute if needed, locates Python
REM               across standard paths, runs legion_prime.py, and pauses.
REM ===============================================================================

setlocal EnableExtensions

REM Change the active directory to the folder containing this batch script
cd /d "%~dp0"
if %errorlevel% neq 0 (
    echo [ERROR] Unable to change directory to "%~dp0".
    pause
    exit /b 1
)

REM Verify that legion_prime.py exists in the project folder
if not exist "%~dp0legion_prime.py" (
    echo [ERROR] Could not find legion_prime.py in "%~dp0".
    pause
    exit /b 1
)

REM Check whether the current session already has Administrator privileges
net session >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Running with Administrator privileges.
    goto :locate_python
)

echo [INFO] Requesting Administrator privileges for Legion Prime...

REM Create a temporary VBScript to trigger a clean native UAC elevation prompt
set "VBS_HELPER=%TEMP%\elevate_legion_%RANDOM%.vbs"
> "%VBS_HELPER%" echo Set UAC = CreateObject("Shell.Application")
>> "%VBS_HELPER%" echo UAC.ShellExecute "cmd.exe", "/c cd /d ""%~dp0"" && ""%~f0""", "", "runas", 1

cscript //nologo "%VBS_HELPER%"
del /f /q "%VBS_HELPER%" >nul 2>&1

REM Exit the original unprivileged window
exit /b 0

:locate_python
set "PYTHON_EXE="

REM 1. Check "py -3" in current PATH
where py >nul 2>&1
if %errorlevel% equ 0 (
    py -3 "%~dp0legion_prime.py"
    goto :after_script
)

REM 2. Check "python" in current PATH
where python >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_EXE=python"
    goto :run_python_script
)

REM 3. Check system-wide and local Python installations
for /f "delims=" %%P in ('dir /b /od "C:\Program Files\Python3*" 2^>nul') do (
    if exist "C:\Program Files\Python3*\python.exe" set "PYTHON_EXE=C:\Program Files\Python3*\python.exe"
)
if defined PYTHON_EXE goto :run_python_script

for /f "delims=" %%P in ('dir /b /od "C:\Python3*" 2^>nul') do (
    if exist "C:\Python3*\python.exe" set "PYTHON_EXE=C:\Python3*\python.exe"
)
if defined PYTHON_EXE goto :run_python_script

if exist "%LocalAppData%\Programs\Python" (
    for /f "delims=" %%D in ('dir /b /ad /od "%LocalAppData%\Programs\Python\Python3*" 2^>nul') do (
        if exist "%LocalAppData%\Programs\Python\%%D\python.exe" (
            set "PYTHON_EXE=%LocalAppData%\Programs\Python\%%D\python.exe"
        )
    )
)
if defined PYTHON_EXE goto :run_python_script

for /f "delims=" %%U in ('dir /b /ad "C:\Users" 2^>nul') do (
    if exist "C:\Users\%%U\AppData\Local\Programs\Python" (
        for /f "delims=" %%D in ('dir /b /ad /od "C:\Users\%%U\AppData\Local\Programs\Python\Python3*" 2^>nul') do (
            if exist "C:\Users\%%U\AppData\Local\Programs\Python\%%D\python.exe" (
                set "PYTHON_EXE=C:\Users\%%U\AppData\Local\Programs\Python\%%D\python.exe"
            )
        )
    )
)
if defined PYTHON_EXE goto :run_python_script

echo [ERROR] Python was not found in PATH or standard installation folders.
echo [INFO] Install Python for all users or add Python to System PATH.
pause
exit /b 1

:run_python_script
echo [INFO] Using Python: "%PYTHON_EXE%"
"%PYTHON_EXE%" "%~dp0legion_prime.py"

:after_script
echo.
echo [INFO] Launcher finished.
pause
endlocal
exit /b 0