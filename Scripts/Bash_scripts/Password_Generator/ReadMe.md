# Simple Password Generator

## Description

This is a simple Bash script designed to generate random passwords of a user-specified length. It leverages the `openssl` utility to produce cryptographically secure random data, which is then Base64 encoded and truncated to the desired length.

## Features

- **User-defined Length:** Allows the user to specify the exact length of the generated password.
- **Cryptographically Secure:** Utilizes `openssl rand` for high-quality randomness.
- **Base64 Character Set:** Generates passwords using characters from the Base64 alphabet (A-Z, a-z, 0-9, +, /), providing a good mix of character types.
- **Concise:** A very short and easy-to-understand script.

## Prerequisites

- A Unix-like operating system (Linux, macOS, WSL).
- `bash` shell (usually pre-installed).
- `openssl` utility (usually pre-installed or easily installable via package manager).
- `cut` utility (usually pre-installed).

## Installation

1. **Save the script:**
    Save the code into a file, for example, `generate_password.sh`.

    ```bash
    nano generate_password.sh
    # Paste the script content and save
    ```

2. **Make it executable:**
    Grant execute permissions to the script:

    ```bash
    chmod +x generate_password.sh
    ```

## Usage

To run the script, open your terminal and execute it:

```bash
./generate_password.sh

The script will then prompt you to enter the desired password length:

This is a simple password generator
Please enter the length of the password:

Enter a number (e.g., 16) and press Enter. The generated password will be displayed.

Example:

This is a simple password generator
Please enter the length of the password:
16
aB3+pQ/xYz7kL9m=

## Important Notes

    Character Set: Passwords generated using Base64 encoding will include alphanumeric characters (A-Z, a-z, 0-9) as well as + (plus) and / (slash) symbols. They may also include = (equals) as padding if the input bytes don't align perfectly, though cut will typically remove these if they are at the end and exceed the desired length.

    Security: While openssl rand provides strong randomness, be aware of the character set limitations if your specific use case requires a different mix of symbols or strictly alphanumeric passwords.

    Alternative (Hexadecimal): The script includes a commented-out line (#openssl rand -hex 48 | cut -c1-$PASS_LENGTH) which would generate passwords using only hexadecimal characters (0-9, a-f). This is generally less secure due to a smaller character set.

## Author

    Wayne Stock

    Initial Date: 2025-07-08
## License

This project is licensed under the MIT License - see the LICENSE.md file for details (if you create one, otherwise specify your preferred license here).
