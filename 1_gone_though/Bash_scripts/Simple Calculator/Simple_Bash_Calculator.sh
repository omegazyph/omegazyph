#!/bin/bash

# ==============================================================================
# SCRIPT NAME:    simple_bash_calculator.sh
# DESCRIPTION:    A CLI calculator that supports decimals using 'bc'.
# AUTHOR:         Wayne Stock
# DATE:           July 30, 2024
# UPDATED:        January 2, 2026
# VERSION:        1.1
# ==============================================================================

# --- Functions ---

# Function to handle the math logic
calculate() {
    # Store arguments into local variables for clarity
    local n1="$1"
    local op="$2"
    local n2="$3"
    local res

    # COMMENT: Check if the 'bc' command exists on this Linux system
    if ! command -v bc &> /dev/null; then
        echo "Error: 'bc' utility is required. Install with: sudo apt install bc"
        return 1
    fi

    # COMMENT: Use a 'case' statement to determine which math operation to run
    case "$op" in
        "+") res=$(echo "scale=4; $n1 + $n2" | bc) ;;
        "-") res=$(echo "scale=4; $n1 - $n2" | bc) ;;
        "*") res=$(echo "scale=4; $n1 * $n2" | bc) ;;
        "/")
            # COMMENT: Check for division by zero before processing
            if (( $(echo "$n2 == 0" | bc) )); then
                echo "Error: Cannot divide by zero."
                return 1
            fi
            res=$(echo "scale=4; $n1 / $n2" | bc)
            ;;
    esac

    # Output the final result to the terminal
    echo "---------------------------"
    echo "Result: $res"
    echo "---------------------------"
}

# --- Main Interaction Loop ---

# Display the header to the user
echo "==================================="
echo "      CLI BASH CALCULATOR"
echo "==================================="
echo "Usage: [number] [operator] [number]"
echo "Example: 10.5 + 5"
echo "Type 'quit' to exit."
echo "==================================="

# COMMENT: Start an infinite loop to allow multiple calculations
while true; do
    # Prompt the user for input
    read -p "Calc > " user_input

    # COMMENT: Convert input to lowercase to check for exit commands
    clean_input=$(echo "$user_input" | tr '[:upper:]' '[:lower:]')
    if [[ "$clean_input" == "q" || "$clean_input" == "quit" || "$clean_input" == "exit" ]]; then
        echo "Goodbye!"
        break
    fi

    # COMMENT: Regex validation
    # This checks for [number] [space] [operator] [space] [number]
    # It supports negative numbers and decimals
    if [[ "$user_input" =~ ^([+-]?[0-9]*\.?[0-9]+)\s*([\+\-\*\/])\s*([+-]?[0-9]*\.?[0-9]+)$ ]]; then
        # Pass the captured regex groups to the calculate function
        calculate "${BASH_REMATCH[1]}" "${BASH_REMATCH[2]}" "${BASH_REMATCH[3]}"
    else
        echo "Invalid format. Please use: 10 + 5"
    fi
    echo "" # Print a newline for readability
done