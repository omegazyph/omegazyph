#!/bin/bash
# Date: 2026-01-10
# Script Name: backup_registry.sh
# Author: omegazyph
# Updated: 2026-01-10
# Description: Backs up the Windows 'Run' registry key to a .reg file 
#              before running the Python spyware scanner.



# Define the registry path and backup destination
REG_PATH="HKCU\Software\Microsoft\Windows\CurrentVersion\Run"
BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/registry_backup_$TIMESTAMP.reg"

# Create the backups directory if it doesn't exist
if [ ! -d "$BACKUP_DIR" ]; then
    mkdir -p "$BACKUP_DIR"
    echo "[*] Created backups directory."
fi

echo "[*] Starting backup of: $REG_PATH"

# Execute the Windows reg export command
# We use reg.exe which is available in the Windows environment
reg.exe export "$REG_PATH" "$BACKUP_FILE" /y

if [ $? -eq 0 ]; then
    echo "[SUCCESS] Backup saved to: $BACKUP_FILE"
    echo "[*] You can now safely run the Python scanner."
else
    echo "[ERROR] Registry backup failed. Please check permissions."
    exit 1
fi