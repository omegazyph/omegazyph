#!/usr/bin/env python3
"""
===============================================================================
Date: 2026-07-23
Script Name: send_facebook_webhook.py
Author: omegazyph
Date Updated: 2026-07-23
Description: This script sends a test alert message from a local crypto bot
             environment to a designated Facebook Messenger recipient using
             the Meta Graph API.
===============================================================================
"""

import sys
import requests


def send_facebook_message(
    message_text: str, page_access_token: str, recipient_id: str
) -> bool:
    """Sends a text message to a Facebook Messenger user via Meta Graph API.

    Parameters:
        message_text (str): The alert message body to be sent.
        page_access_token (str): The Facebook Page Access Token with
        messaging permissions. recipient_id (str): The PSID (Page-Scoped ID) of
        the recipient.

    Returns:
        bool: True if the request was successful, False otherwise.
    """
    # Meta Graph API endpoint for sending messages
    api_url = f"https://graph.facebook.com/v21.0/me/messages"

    # Define query parameters including the access token
    params = {"access_token": page_access_token}

    # Set up headers for JSON payload transmission
    headers = {"Content-Type": "application/json"}

    # Construct the required JSON payload for Facebook Messenger
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text},
        "messaging_type": "RESPONSE",
    }

    try:
        # Send HTTP POST request to Facebook Graph API
        response = requests.post(
            api_url, params=params, headers=headers, json=payload, timeout=10
        )

        # Raise an exception for HTTP error response codes
        response.raise_for_status()

        # Parse JSON response
        response_data = response.json()
        print("Successfully sent message to Facebook Messenger.")
        print(f"Recipient ID: {response_data.get('recipient_id')}")
        print(f"Message ID: {response_data.get('message_id')}")
        return True

    except requests.exceptions.HTTPError as http_error:
        print(f"HTTP error occurred while sending message: {http_error}")
        print(f"Response Body: {response.text}")
        return False
    except requests.exceptions.RequestException as request_error:
        print(f"Network error occurred while sending message: {request_error}")
        return False


def main() -> None:
    """Main execution function to test the webhook notification script."""
    # Replace the placeholder credentials below with your actual Facebook Page Access Token
    # and Page-Scoped User ID (PSID).
    page_access_token = "YOUR_FACEBOOK_PAGE_ACCESS_TOKEN"
    recipient_id = "YOUR_RECIPIENT_PAGE_SCOPED_ID"

    # Check if user updated placeholders before running
    if (
        page_access_token == "YOUR_FACEBOOK_PAGE_ACCESS_TOKEN"
        or recipient_id == "YOUR_RECIPIENT_PAGE_SCOPED_ID"
    ):
        print("Error: Please set your actual page_access_token and recipient_id.")
        sys.exit(1)

    # Define the test message payload
    test_message = "Crypto Bot Alert: Test notification triggered successfully!"

    print("Attempting to send test webhook notification...")
    send_facebook_message(
        message_text=test_message,
        page_access_token=page_access_token,
        recipient_id=recipient_id,
    )


if __name__ == "__main__":
    main()