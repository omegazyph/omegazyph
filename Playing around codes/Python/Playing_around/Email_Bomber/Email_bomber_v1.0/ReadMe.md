# Email Bomber

## Description
Email Bomber is a Python script designed to send a large number of emails to a target email address. It can be used for testing the resilience of email servers or for educational purposes.

## Features
- Allows the user to specify the target email address.
- Offers different bombing modes with preset numbers of emails to send.
- Supports customization of the bombing mode with a custom number of emails.
- Provides options to select from premade email server configurations or to enter custom settings.
- Includes a simple user interface for entering sender's email address, password, subject, and message.
- Utilizes the smtplib module for sending emails via SMTP.

## Requirements
- Python 3.x
- smtplib module

## Usage
1. Clone or download the script to your local machine.
2. Open a terminal or command prompt and navigate to the directory containing the script.
3. Run the script using Python 3:
    ```
    python3 email_bomber_V1.0.py 
    or
    python email_bomber_V1.0.py
    both or one should work for you
    ```
4. Follow the prompts to enter the target email address, bombing mode, email server configuration, sender's email address, password, subject, and message.
5. Once all parameters are set, the script will initiate the email bombing attack.

## Disclaimer
This script is provided for educational and testing purposes only. Misuse of this script for sending unsolicited or malicious emails is illegal and unethical. The author takes no responsibility for any misuse of this script.
!!!This will not bypass the 2FA!!!

## Author
[Omegazyph]

## Version
1.0

## License
This project is licensed under the [MIT License](LICENSE).
