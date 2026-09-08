########################################################################################
# Date: 2026-09-08
# Script Name: ascii_art1.py
# Author: Wayne Stock
# Updated: 2026-09-08
# Description: Generates ASCII art banners with an interactive menu to choose fonts.
########################################################################################

import pyfiglet

# Define available font options in a dictionary
available_fonts = {
    "1": ("slant", "Slant"),
    "2": ("standard", "Standard"),
    "3": ("banner3-D", "3D Banner"),
    "4": ("block", "Block"),
    "5": ("digital", "Digital"),
}

# Prompt user for input text
user_text = input("Enter the text for your banner: ")

# Display font choices
print("\nSelect a font style:")
for key, font_info in available_fonts.items():
    print(key + ". " + font_info[1])

# Get user choice
choice = input("\nEnter choice (1-5): ")

# Determine chosen font, defaulting to 'slant' if selection is invalid
if choice in available_fonts:
    selected_font = available_fonts[choice][0]
else:
    print("\nInvalid choice. Defaulting to 'slant' font.")
    selected_font = "slant"

# Generate and print ASCII art
print("\n")
banner_art = pyfiglet.figlet_format(user_text, font=selected_font)
print(banner_art)