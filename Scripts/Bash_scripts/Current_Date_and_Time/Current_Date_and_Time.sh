#!/bin/bash

# ==============================================================================
# SCRIPT NAME:    Current_Date_and_Time.sh
# DESCRIPTION:    A simple starter Bash script to demonstrate basic features.
# AUTHOR:         Wayne Stock
# DATE:           July 30, 2025
# VERSION:        1.1
# ==============================================================================

# REMOVED THE SPACE after the '=' to fix the assignment error
CURRENT_DATE=$(date +%Y-%m-%d)
echo "Today's date is: $CURRENT_DATE"

# Displaying time for the user
TIMESTAMP=$(date +%r)
echo "Current timestamp: $TIMESTAMP"

# USE A CLEANER TIMESTAMP FOR FILENAMES
# This replaces colons and spaces with underscores so it doesn't break files
FILE_TIME=$(date +%H_%M_%S)
LOG_FILE="mylog_${CURRENT_DATE}_${FILE_TIME}.log"

echo "Log file will be: $LOG_FILE"
touch "$LOG_FILE"