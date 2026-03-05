#!/bin/bash

################################################################################
# Date: 2026-01-08
# Script Name: backup_system.sh
# Author: omegazyph
# Updated: 2026-01-08
# Description: Automates the compression and archiving of local directories.
#              Includes a retention policy to delete files older than 7 days.
################################################################################

# --- Configuration ---
# Change these paths to match your WSL environment
SOURCE_DIR="/home/omegazyph/projects"
BACKUP_DIR="/home/omegazyph/backups"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_NAME="backup_$TIMESTAMP.tar.gz"
RETENTION_DAYS=7

# --- Logic ---

# 1. Create the backup directory if it doesn't exist
if [ ! -d "$BACKUP_DIR" ]; then
    echo "Creating backup directory at $BACKUP_DIR..."
    mkdir -p "$BACKUP_DIR"
fi

# 2. Compress the source directory
echo "Starting backup of $SOURCE_DIR..."
tar -czf "$BACKUP_DIR/$BACKUP_NAME" "$SOURCE_DIR"

# Check if the tar command succeeded
if [ $? -eq 0 ]; then
    echo "Backup successful: $BACKUP_NAME"
else
    echo "Backup failed!"
    exit 1
fi

# 3. Cleanup: Delete backups older than $RETENTION_DAYS
echo "Cleaning up backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -type f -name "backup_*.tar.gz" -mtime +$RETENTION_DAYS -exec rm {} \;

echo "Maintenance complete."