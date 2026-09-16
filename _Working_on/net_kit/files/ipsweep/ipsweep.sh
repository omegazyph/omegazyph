#!/usr/bin/env bash
# ===========================================================================================
# Date:         2026-09-13
# Script Name:  ipsweep.sh
# Author:       Omegazyph
# Updated:      2026-09-16
# Description:  ipsweep runs through IP addresses based on user input or command-line argument.
# ===========================================================================================

# Difine the target file to log the ip 
TARGET_FILE="results/ip_list.txt"

# Function to prompt the user and handle the choice
get_user_choice(){
    local user_input=""
    local target_subnet=""

    # Keep looping until the user enters a valid choice
    while true; do
        echo -ne "${BOLD}${YELLOW}Are you using Kali or Windows? [Kali/Windows]: ${RESET}"
        read -r user_input

        # Check for Kali (supporting lowercase or capitalized inputs)
        if [ "$user_input" = "Kali" ] || [ "$user_input" = "kali" ] || [ "$user_input" = "Windows" ] || [ "$user_input" = "windows" ]; then
            break
        else
            echo -e "${BOLD}${RED}[X] Invalid choice. Please type exactly 'Kali' or 'Windows'.${RESET}"
        fi
    done

    # Prompt for the subnet from the user
    echo -ne "Enter the target subnet (e.g., 192.168.0): "
    read -r target_subnet

    # Run the correct function base on what was chosen and pass the subnet
    if [ "$user_input" = "Kali" ] || [ "$user_input" = "kali" ]; then
        echo "Selection confirmed : Kali"
        Kali "$target_subnet"
    else
        echo "Selection confirmed: Windows"
        windows "$target_subnet"
    fi

}


# for Kali or alike
Kali(){
    local target_subnet="$1" 

    # Loop through numbers 1 to 254 to use as the last octet of the IP address
    for ip in $(seq 1 254); do
        # Display inline status Bar
        printf "${CYAN}\r[*] Scanning: %s.%s (%d/254) ${RESET}\n" "$target_subnet" "$ip" "$ip"
        
        # Ping the target IP address once (-c 1), filter for successful replies, and extract the IP
        if ping -c 4 "$target_subnet.$ip" | grep "64 bytes"; then
            echo -e "$target_subnet.$ip" >> "$TARGET_FILE"
            print_message "success" "Host is alive\n"
        else
            print_message "error" "Nothing Here\n"
                    fi
    done
}

# for windows
windows(){
    for ip in $(seq 1 254); do
        # Display inline status bar
        printf "${CYAN}\r[*] Scanning: %s.%s (%d/254) ${RESET}\n" "$1" "$ip" "$ip"
        
        if ping "$1.$ip" | grep -q "bytes=32" ; then
            echo -e "$1.$ip" >> "$TARGET_FILE"
            print_message "success" "Host is alive\n"
        else
            print_message "error" "Nothing Here\n"

    fi
    done
}



# --- Main Function ---
get_user_choice