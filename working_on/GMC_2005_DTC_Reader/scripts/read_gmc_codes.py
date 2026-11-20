#!/usr/bin/env python

#==================================================================================
#   Date: 2026-11-19
#   Script Name: read_gmc_codes.py
#   Author: omegazyph
#   Updated: 2026-11-19
#   Description: Connects to an OBDLink MX+ Bluetooth adapter on Windows and reads
#             Stored (Mode 03) and Pending (Mode 07) Diagnostic Trouble Codes
#             from a 2005 GMC Sierra 2500HD using the SAE J1850 VPW protocol.
#             Saves the results to a log file and offers an option to clear codes.
#==================================================================================

# --- Imports ---
import time
from datetime import datetime
from pathlib import Path

import serial
import serial.tools.list_ports

# --- ANSI Color Codes ---
BLUE = "\033[1;34m"
BOLD = "\033[1m"
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
PURPLE = "\033[1;35m"
RED = "\033[1;31m"
RESET = "\033[0m"
YELLOW = "\033[1;33m"

# Common GM Class 2 module addresses so you know which computer reported the code
MODULE_NAMES = {
    "10": "Powertrain Control Module (PCM / Engine)",
    "18": "Transmission Control Module (TCM / Allison)",
    "28": "Electronic Brake Control Module (EBCM / ABS)",
    "40": "Body Control Module (BCM)",
    "58": "Airbag / Supplemental Inflatable Restraint (SDM)",
    "60": "Instrument Panel Cluster (IPC)",
}

# --- UI Functions ---

def print_ascii_banner(banner_title="Default Title Starting"):
    """Prints a dynamically centered starting ASCII banner."""
    total_width = 80
    title_length = len(banner_title)
    padding = (total_width - title_length) // 2

    # Generate the exact amount of leading spaces for centering
    spaces = " " * padding

    separator_line = "=" * total_width

    print(f"{PURPLE}{separator_line}{RESET}")
    print(f"{BOLD}{BLUE}{spaces}{banner_title}{RESET}")
    print(f"{PURPLE}{separator_line}{RESET}")


def print_ascii_ending(ending_title="Default Title Ending"):
    """Prints a dynamically centered closing ASCII banner."""
    total_width = 80
    title_length = len(ending_title)
    padding = (total_width - title_length) // 2

    # Generate the exact amount of leading spaces for centering
    spaces = " " * padding

    separator_line = "=" * total_width

    print(f"{PURPLE}{separator_line}{RESET}")
    print(f"{BOLD}{BLUE}{spaces}{ending_title}{RESET}")
    print(f"{PURPLE}{separator_line}{RESET}")


def print_message(message_type, message_text=""):
    """Unified message printing function using ANSI color formatting."""
    if message_type == "error":
        print(f"{BOLD}{RED}[X] {message_text}{RESET}")
    elif message_type == "info":
        print(f"{BOLD}{BLUE}[*] {message_text}{RESET}")
    elif message_type == "status":
        print(f"{BOLD}{CYAN}[*] {message_text}{RESET}")
    elif message_type == "success":
        print(f"{BOLD}{GREEN}[+] {message_text}{RESET}")
    elif message_type == "warning":
        print(f"{BOLD}{YELLOW}[!] {message_text}{RESET}")
    else:
        print(message_text)





def find_windows_com_ports() -> list[str]:
    """Lists all active serial COM ports available on Windows."""
    detected_ports = serial.tools.list_ports.comports()
    port_list = []

    print("\n--- Available Windows COM Ports ---")
    if not detected_ports:
        print("  [NONE] No COM ports found. Check that your OBDLink MX+ is paired.")
        return port_list

    for port_entry in detected_ports:
        port_list.append(port_entry.device)
        print(f"  {port_entry.device} -> {port_entry.description}")

    return port_list


def send_command_to_adapter(
    connection: serial.Serial,
    command_text: str,
    delay_seconds: float = 0.5,
) -> list[str]:
    """
    Sends a single AT or OBD-II command to the OBDLink MX+ and waits for
    the '>' ready prompt before returning cleaned response lines.
    """
    connection.reset_input_buffer()

    encoded_command = f"{command_text.strip()}\r".encode("ascii")
    connection.write(encoded_command)
    time.sleep(delay_seconds)

    response_bytes = bytearray()
    deadline = time.time() + 5.0

    while time.time() < deadline:
        if connection.in_waiting > 0:
            chunk = connection.read(connection.in_waiting)
            response_bytes.extend(chunk)
            if b">" in response_bytes:
                break
        else:
            time.sleep(0.05)

    decoded_output = response_bytes.decode("ascii", errors="ignore")
    cleaned_lines = []

    for raw_line in decoded_output.splitlines():
        line = raw_line.replace(">", "").strip()
        if line and line != command_text.strip():
            cleaned_lines.append(line)

    return cleaned_lines


def setup_mx_plus_for_2005_gmc(connection: serial.Serial) -> None:
    """Resets the OBDLink MX+ and locks it to SAE J1850 VPW (Protocol 2)."""
    print("\n--- Connecting to OBDLink MX+ ---")

    reset_reply = send_command_to_adapter(connection, "ATZ", delay_seconds=1.2)
    print(f"  Adapter ID      : {' '.join(reset_reply)}")

    # Disable command echo
    send_command_to_adapter(connection, "ATE0", delay_seconds=0.3)

    # Enable headers so we can see which module (Engine, Trans, ABS) sent each code
    send_command_to_adapter(connection, "ATH1", delay_seconds=0.3)

    # Enable spaces between hexadecimal bytes
    send_command_to_adapter(connection, "ATS1", delay_seconds=0.3)

    # Lock Protocol 2: SAE J1850 VPW (used by 2005 GMC Sierra)
    protocol_reply = send_command_to_adapter(connection, "ATSP2", delay_seconds=0.5)
    print(f"  Protocol Locked : {' '.join(protocol_reply)} (SAE J1850 VPW)")

    # Read truck battery voltage from the OBD-II port
    voltage_reply = send_command_to_adapter(connection, "ATRV", delay_seconds=0.5)
    print(f"  Battery Voltage : {' '.join(voltage_reply)}")


def convert_hex_pair_to_dtc(first_byte_hex: str, second_byte_hex: str) -> str:
    """
    Translates a 2-byte hexadecimal trouble code into standard OBD-II format
    (for example: '03' and '00' becomes 'P0300').
    """
    high_nibble = int(first_byte_hex[0], 16)
    prefix_lookup = {
        0: "P0",
        1: "P1",
        2: "P2",
        3: "P3",
        4: "C0",
        5: "C1",
        6: "C2",
        7: "C3",
        8: "B0",
        9: "B1",
        10: "B2",
        11: "B3",
        12: "U0",
        13: "U1",
        14: "U2",
        15: "U3",
    }
    code_prefix = prefix_lookup.get(high_nibble, "P0")
    code_digits = f"{first_byte_hex[1]}{second_byte_hex}"
    return f"{code_prefix}{code_digits}"


def extract_codes_from_frames(
    response_lines: list[str],
    service_response_byte: str,
) -> list[dict[str, str]]:
    """
    Parses J1850 VPW frames with headers enabled and returns a list of
    dictionaries containing each DTC and the module that reported it.
    """
    found_entries = []

    for line in response_lines:
        if any(keyword in line for keyword in ("NO DATA", "ERROR", "UNABLE", "STOPPED")):
            continue

        tokens = line.split()
        # With ATH1 enabled, a J1850 VPW frame is structured as:
        # [Priority] [Target] [Source Module] [Service Byte (43 or 47)] [DTC Bytes...] [Checksum]
        if len(tokens) >= 6 and service_response_byte in tokens:
            source_module_hex = tokens[2].upper()
            module_label = MODULE_NAMES.get(
                source_module_hex,
                f"Module 0x{source_module_hex}",
            )

            service_index = tokens.index(service_response_byte)
            # Slice between the service byte and the final 1-byte checksum
            dtc_bytes = tokens[service_index + 1 : -1]

            position = 0
            while position + 1 < len(dtc_bytes):
                byte_one = dtc_bytes[position]
                byte_two = dtc_bytes[position + 1]

                if byte_one != "00" or byte_two != "00":
                    dtc_string = convert_hex_pair_to_dtc(byte_one, byte_two)
                    entry = {
                        "code": dtc_string,
                        "module": module_label,
                    }
                    if entry not in found_entries:
                        found_entries.append(entry)

                position += 2

    return found_entries


def read_all_trouble_codes(connection: serial.Serial) -> dict[str, list[dict[str, str]]]:
    """Requests Stored (Mode 03) and Pending (Mode 07) codes from the truck."""
    print("\n--- Scanning Truck for Diagnostic Trouble Codes ---")

    # Mode 03: Confirmed / Stored DTCs that trigger the Check Engine Light
    stored_lines = send_command_to_adapter(connection, "03", delay_seconds=1.5)
    stored_codes = extract_codes_from_frames(stored_lines, service_response_byte="43")

    # Mode 07: Pending DTCs detected during the current or last drive cycle
    pending_lines = send_command_to_adapter(connection, "07", delay_seconds=1.5)
    pending_codes = extract_codes_from_frames(pending_lines, service_response_byte="47")

    print("\n[STORED CODES - Mode 03]")
    if stored_codes:
        for item in stored_codes:
            print(f"  * {item['code']}  (Reported by: {item['module']})")
    else:
        print("  None found.")

    print("\n[PENDING CODES - Mode 07]")
    if pending_codes:
        for item in pending_codes:
            print(f"  * {item['code']}  (Reported by: {item['module']})")
    else:
        print("  None found.")

    return {
        "stored": stored_codes,
        "pending": pending_codes,
    }


def clear_trouble_codes(connection: serial.Serial) -> None:
    """Sends Mode 04 to clear stored/pending DTCs and turn off the Check Engine Light."""
    print("\n--- Clearing Diagnostic Trouble Codes ---")
    clear_reply = send_command_to_adapter(connection, "04", delay_seconds=1.5)
    print(f"  Clear Command Response: {clear_reply}")
    print("  [DONE] Reset command sent. Cycle the ignition key off for 10 seconds.")


def write_code_log_file(
    com_port: str,
    scan_results: dict[str, list[dict[str, str]]],
) -> Path:
    """Saves the trouble code report to the logs folder for your repair notes."""
    project_folder = Path(__file__).resolve().parent.parent
    logs_folder = project_folder / "logs"
    logs_folder.mkdir(parents=True, exist_ok=True)

    file_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_path = logs_folder / f"gmc_dtc_report_{file_timestamp}.txt"

    with log_file_path.open("w", encoding="utf-8") as log_file:
        log_file.write("2005 GMC Sierra 2500HD - Diagnostic Trouble Code Report\n")
        log_file.write(f"Scan Time : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"COM Port  : {com_port}\n")
        log_file.write("=" * 60 + "\n\n")

        log_file.write("STORED CODES (Mode 03):\n")
        if scan_results["stored"]:
            for item in scan_results["stored"]:
                log_file.write(f"  - {item['code']} | {item['module']}\n")
        else:
            log_file.write("  None\n")

        log_file.write("\nPENDING CODES (Mode 07):\n")
        if scan_results["pending"]:
            for item in scan_results["pending"]:
                log_file.write(f"  - {item['code']} | {item['module']}\n")
        else:
            log_file.write("  None\n")

    print(f"\n[LOG SAVED] Report saved to: {log_file_path}")
    return log_file_path



# --- Main Process ---



def main() -> None:
    """Main entry point for reading and optionally clearing 2005 GMC trouble codes."""
    # Display the starup Banner
    print_ascii_banner("2005 GMC Sierra 2500HD - Diagnostic Trouble Code Reader")
    

    available_ports = find_windows_com_ports()
    if not available_ports:
        return

    chosen_port = input("\nEnter your OBDLink MX+ COM port (e.g., COM4): ").strip().upper()
    if not chosen_port:
        print("[CANCELLED] No COM port entered.")
        return

    try:
        with serial.Serial(
            port=chosen_port,
            baudrate=115200,
            timeout=1.0,
            write_timeout=1.0,
        ) as obd_port:
            setup_mx_plus_for_2005_gmc(obd_port)
            results = read_all_trouble_codes(obd_port)
            write_code_log_file(chosen_port, results)

            if results["stored"] or results["pending"]:
                user_choice = input(
                    "\nDo you want to CLEAR these codes now? (type YES to clear, or press Enter to skip): "
                ).strip().upper()
                if user_choice == "YES":
                    clear_trouble_codes(obd_port)
                else:
                    print("[KEPT] Trouble codes were left untouched.")

    except serial.SerialException as serial_error:
        print(f"\n[CONNECTION ERROR] Could not open {chosen_port}: {serial_error}")
        print("Make sure the OBDLink MX+ is plugged into the truck, the key is in RUN,")
        print("and no other OBD app is connected to that COM port.")


if __name__ == "__main__":
    main()