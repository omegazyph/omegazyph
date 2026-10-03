#!/bin/bash
# Date: 2026-10-02
# Script Name: check_ip_webhook.sh
# Author: omegazyph
# Updated: 2026-10-02
# Description: Checks the current public IP address against a local saved copy.
#              If a change is detected, it sends a Webhook notification and updates the file.

# Define project folder structure and files
PROJECT_DIR="$HOME/ip_checker"
DATA_DIR="$PROJECT_DIR/data"
LOG_DIR="$PROJECT_DIR/logs"

# Ensure directories exist
mkdir -p "$DATA_DIR" "$LOG_DIR"

# File paths
IP_FILE="$DATA_DIR/current_ip.txt"
LOG_FILE="$LOG_DIR/ip_check.log"

# Replace this URL with your actual Webhook endpoint (e.g., Discord or custom listener)
WEBHOOK_URL="https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"

# Retrieve current public IP address
CURRENT_IP=$(curl -s https://ifconfig.me)

# Check if curl succeeded in retrieving an IP
if [ -z "$CURRENT_IP" ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Error: Unable to fetch public IP." >> "$LOG_FILE"
    exit 1
fi

# Check if the IP history file exists
if [ -f "$IP_FILE" ]; then
    SAVED_IP=$(cat "$IP_FILE")
else
    SAVED_IP=""
fi

# Compare the current IP with the saved IP
if [ "$CURRENT_IP" != "$SAVED_IP" ]; then
    # Create JSON payload for the webhook notification
    MESSAGE="{\"content\": \"⚠️ **Server IP Changed!**\\n**Old IP:** ${SAVED_IP:-None}\\n**New IP:** ${CURRENT_IP}\"}"

    # Send notification via Webhook POST request
    HTTP_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -H "Content-Type: application/json" -X POST -d "$MESSAGE" "$WEBHOOK_URL")

    # Verify if webhook was delivered successfully
    if [ "$HTTP_RESPONSE" -eq 200 ] || [ "$HTTP_RESPONSE" -eq 204 ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - IP changed from '$SAVED_IP' to '$CURRENT_IP'. Webhook notification sent." >> "$LOG_FILE"
        # Update the stored IP address
        echo "$CURRENT_IP" > "$IP_FILE"
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') - IP changed to '$CURRENT_IP', but webhook failed with HTTP status code $HTTP_RESPONSE." >> "$LOG_FILE"
    fi
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - IP unchanged ($CURRENT_IP)." >> "$LOG_FILE"
fi