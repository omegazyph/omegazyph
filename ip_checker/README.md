# IP Address Monitor & Webhook Notifier

A lightweight, automated Bash utility designed to monitor your server's public IP address for changes and instantly issue alerts via Webhook (e.g., Discord). This tool is particularly useful for hosted bots, services, or scripts running on dynamic IP residential networks.

---

## Features

- **Automated IP Checking**: Fetches your external public IP using lightweight cURL requests.
- **Webhook Integration**: Posts instant status alerts when your public IP changes.
- **State Persistence**: Remembers the last confirmed IP in a dedicated data directory to prevent duplicate alerts.
- **Comprehensive Logging**: Maintains timestamps and logs for check-ins and delivery status.
- **Cron Ready**: Easily scheduled for automated background monitoring.

---

## Folder Structure

For optimal organization, set up the project directory as follows:

```text
ip_checker/
├── check_ip_webhook.sh
├── README.md
├── data/
│   └── current_ip.txt
└── logs/
    └── ip_check.log
```

---

## Installation & Setup

### 1. Clone or Create Project Files

Create your working directory and directory structure:

```bash
mkdir -p ~/ip_checker/data ~/ip_checker/logs
cd ~/ip_checker
```

### 2. Configure the Script

Open `check_ip_webhook.sh` in your editor and update the `WEBHOOK_URL` variable with your actual webhook endpoint:

```bash
WEBHOOK_URL="https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"
```

### 3. Grant Execution Permissions

Make the script executable:

```bash
chmod +x check_ip_webhook.sh
```

---

## Usage

### Testing

Run the script manually to ensure it successfully detects your IP address and triggers your webhook:

```bash
./check_ip_webhook.sh
```

Inspect the logs to verify output:

```bash
cat logs/ip_check.log
```

---

## Automated Monitoring (Cron Job)

To run the check automatically in the background (e.g., every 15 minutes):

1. Open your crontab editor:

   ```bash
   crontab -e
   ```

2. Add the following entry at the bottom of the file (replace `/path/to/` with your actual full directory path):

   ```cron
   */15 * * * * /bin/bash /path/to/ip_checker/check_ip_webhook.sh
   ```

---

## Customization

- **Change Check Frequency**: Adjust the cron timing (e.g., `*/5 * * * *` for every 5 minutes or `0 * * * *` for hourly).
- **Custom Payloads**: Modify the `$MESSAGE` variable inside `check_ip_webhook.sh` to adjust the formatting or add extra parameters for your specific webhook consumer.
