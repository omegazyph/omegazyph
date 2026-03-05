#!/bin/bash
# Author: Wayne Stock 
# Date: 2025-07-08 

# Script Name: simple_password_generator.sh
# Description: This script generates a random password of a specified length
#              using the OpenSSL utility. It utilizes base64 encoding to ensure
#              a diverse set of characters (alphanumeric, symbols).

# --- Start of Script ---

# Display a user-friendly message indicating the script's purpose.
echo "This is a simple password generator"

# Prompt the user to enter the desired length for the password.
echo "Please enter the length of the password:"

# Read the user's input and store it in the variable PASS_LENGTH.
# The 'read' command waits for user input until Enter is pressed.
read PASS_LENGTH

# The 'for' loop is set to iterate only once (from 1 to 1).
# Although a loop isn't strictly necessary for a single password generation,
# it's a common pattern if you intended to generate multiple passwords,
# which could be achieved by changing 'seq 1' to 'seq N' (e.g., 'seq 5').
for p in $(seq 1);
do
    # Generate a random string using OpenSSL:
    # 'openssl rand -base64 48': Generates 48 bytes of cryptographically secure
    #                         random data and encodes it using Base64.
    #                         Base64 characters include A-Z, a-z, 0-9, '+', '/', and '=' (padding).
    #                         48 bytes of Base64 encoded data will result in 64 characters
    #                         (48 * 8 bits / 6 bits per Base64 char = 64 characters before padding).
    #
    # 'cut -c1-$PASS_LENGTH': Takes the output from 'openssl rand' and cuts it.
    #                         '-c1-$PASS_LENGTH' specifies to extract characters
    #                         from the 1st position up to the length specified by PASS_LENGTH.
    #                         This effectively truncates the 64-character base64 string
    #                         to the user's desired password length.
    openssl rand -base64 48 | cut -c1-$PASS_LENGTH

        # The following line is commented out but provides an alternative for generating
        # passwords using hexadecimal characters (0-9, a-f).
        # It's noted as "does not follow the rules" likely because it generates passwords
        # with a more limited character set (only hex digits), which might not meet
        # common password complexity requirements (e.g., requiring symbols, mixed case).
    # openssl rand -hex 48 | cut -c1-$PASS_LENGTH
done

# --- End of Script ---