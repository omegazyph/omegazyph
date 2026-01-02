#!/bin/bash

# ==============================================================================
# SCRIPT NAME:    Login_Gate_2.sh
# DESCRIPTION:    A simple login
#                   added a while loop form Login_gate1
# AUTHOR:         Wayne Stock
# DATE:           Jan 2, 2026
# VERSION:        1.1
# USAGE:          ./Login_Gate_2.sh
# ==============================================================================



#key
user="Wayne"
pass="12345"

# attempts
attempts=3

# added a while loop for attempts
while [[ $attempts -gt 0 ]]; do
    
    # Entery
    # this way is cleaner then using Echo
    read -p "Please Enter your username: " name
    # for passwords us -sp it will hide the password in the screen 
    read -sp "Please Enter your password: " password

    # if statement to check the key and the user input
    if [[ $user == $name && $pass == $password ]]; then
        echo -e "\nAccess Granted"
        exit 0
    else 
        # the -e is for enable the newline simble
        echo -e "\nAccess Denied"
        ((attempts--))
    fi
done

# last word 
echo "I'm Calling your Mother"
