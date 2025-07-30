#!/bin/bash

# ==============================================================================
# SCRIPT NAME:    Current_Date_and_Time.sh
# DESCRIPTION:    A simple starter Bash script to demonstrate basic features.
# AUTHOR:         Wayne Stock
# DATE:           July 30, 2025
# VERSION:        1.0
# USAGE:          ./Current_Date_and_Time.sh
# ==============================================================================


CURRENT_DATE=$(date +%Y-%m-%d)
echo "Today's date is: $CURRENT_DATE"

TIMESTAMP=$(date +%r)
echo "Current timestamp: $TIMESTAMP"

# Use it in a filename
LOG_FILE="mylog_${TIMESTAMP}.log"
echo "Log file will be: $LOG_FILE"
touch "$LOG_FILE" # Create an empty log file with that name