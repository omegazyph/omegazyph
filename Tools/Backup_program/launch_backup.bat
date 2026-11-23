@echo off
REM ===============================================================================
REM Project Folder Structure:
REM   Legion-External-Backup/
REM     ├── README.md
REM     ├── launch_backup.bat
REM     ├── backup_config.json
REM     └── legion_to_external_backup.py
REM
REM Date:         2026-11-23
REM Script Name:  launch_backup.bat
REM Author:       omegazyph
REM Description:  Changes to the project directory and launches
REM               legion_to_external_backup.py in a Windows command prompt.
REM ===============================================================================

REM Move to the directory where this batch file is located so relative paths resolve cleanly
cd /d "%~dp0"

REM Verify that the Python script exists before attempting execution
if not exist "legion_to_external_backup.py" (
    echo [X] Error: legion_to_external_backup.py not found in "%~dp0".
    pause
    exit /b 1
)

REM Run the backup script using the python executable
python "legion_to_external_backup.py"

REM Pause at the end so banner output and summary counts remain visible
pause
exit /b 0