#!/bin/bash

# ==============================================================================
# SCRIPT NAME:    Login_Gate_1.sh
# DESCRIPTION:    A simple login
# AUTHOR:         Wayne Stock
# DATE:           Jan 2, 2026
# VERSION:        1.0
# USAGE:          ./Simple_Login_Gate.sh
# ==============================================================================


# Entery
# this way is cleaner then using Echo
read -p "Please Enter your username: " name
# for passwords us -sp it will hide the password in the screen 
read -sp "Please Enter your password: " password

#key
user="Wayne"
pass="12345"


# if statement to check the key and the user input
if [[ $user == $name && $pass == $password ]]; then
    echo -e "\nAccess Granted"
else 
    # the -e is for enable the newline simble
    echo -e "\nDenied"
fi