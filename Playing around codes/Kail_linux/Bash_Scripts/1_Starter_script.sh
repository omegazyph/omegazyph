#!/bin/bash

# ==============================================================================
# SCRIPT NAME:    my_first_script.sh
# DESCRIPTION:    A simple starter Bash script to demonstrate basic features.
# AUTHOR:         [Your Name/Alias]
# DATE:           July 30, 2025
# VERSION:        1.0
# USAGE:          ./my_first_script.sh
# ==============================================================================

# --- 1. Shebang Line ---
# The line above (#!/bin/bash) is called the "shebang."
# It tells the operating system which interpreter to use to execute the script.
# In this case, it's Bash, located at /bin/bash.

# --- 2. Comments ---
# Lines starting with '#' are comments. They are ignored by the interpreter
# and are used to explain what the script does or what specific lines mean.
# Good commenting makes your script understandable to others and your future self!

# --- 3. Variables ---
# Variables store data. You don't declare types in Bash; just assign.
# No spaces around the '=' when assigning.
MY_NAME="Bash User"
CURRENT_YEAR=$(date +%Y) # Command substitution: runs `date +%Y` and stores its output.
LOG_FILE="script_log.txt"

# --- 4. Basic Output (echo) ---
echo "Hello, $MY_NAME!" # Double quotes allow variable expansion. Single quotes don't.
echo "This is your first Bash script."
echo "Running in the year: $CURRENT_YEAR"
echo "" # Prints an empty line for spacing

# --- 5. Conditional Statements (if/else) ---
# Check if a file exists.
if [ -f "$LOG_FILE" ]; then
    echo "Log file '$LOG_FILE' already exists."
else
    echo "Log file '$LOG_FILE' does not exist. Creating it now..."
    touch "$LOG_FILE" # Create an empty file
fi

# --- 6. Writing to a file (redirection) ---
echo "$(date): Script started." >> "$LOG_FILE" # Appends output to the log file

# --- 7. User Input ---
read -p "What is your favorite color? " FAV_COLOR
echo "Ah, $FAV_COLOR is a great color!"

# --- 8. Loops (for loop) ---
echo "Counting to 3:"
for i in 1 2 3; do
    echo "Number: $i"
    sleep 0.5 # Pause for 0.5 seconds
done

# --- 9. Functions ---
# Functions help organize your code and reuse blocks of logic.
greet_user() {
    local name=$1 # 'local' makes the variable specific to the function
    echo "Greetings, $name! Nice to see you."
}

greet_user "Buddy"
greet_user "Explorer"

# --- 10. Command Execution ---
echo ""
echo "Listing current directory contents:"
ls -lh # Execute the 'ls' command with options

# --- 11. Error Handling / Exit Status ---
# Every command returns an "exit status" (0 for success, non-zero for failure).
# You can check this using $?
# Example: Try a command that might fail
echo "Attempting to list a non-existent directory..."
ls /this/path/does/not/exist &>/dev/null # Suppress output for demonstration
if [ $? -ne 0 ]; then # $? holds the exit status of the *last* executed command
    echo "  (Command failed as expected!)"
fi

# --- 12. End of Script ---
echo ""
echo "$(date): Script finished." >> "$LOG_FILE" # Append final message
echo "Script execution complete. Check '$LOG_FILE' for log entries."

# Exit with a success status (0).
exit 0