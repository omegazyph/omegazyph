#!/usr/bin/env bash
###########################################################################
# Date:         2026-01-04
# Script Name:  Downloads_CleanBot.sh
# Author:       Omegazyph
# Updated:      2026-09-11
# Description:  A system utility to automatically organize 
#               the Downloads folder by file extension.
###########################################################################

# ANSI Color Codes
BOLD='\033[1m'
CYAN='\033[1;36m'
GREEN='\033[1;32m'
BLUE='\033[1;34m'
PURPLE='\033[1;35m'
YELLOW='\033[1;33m'
RED='\033[1;31m'
RESET='\033[0m'

# SETTINGS
TARGET_DIR="$HOME/Downloads"
TARGET_FOLDERS=("Pictures" "Documents" "Music" "Videos" "Compressed")

# Start shopt
shopt -s nullglob

# Output Functions
print_ascii_banner() {
    echo -e "${CYAN}====================================================${RESET}"
    echo -e "${BOLD}${CYAN}            DOWNLOADS_CLEANBOT - INITIATED       ${RESET}"
    echo -e "${CYAN}====================================================${RESET}"
}

print_status() {
    echo -e "\n${BOLD}${CYAN}[*] $1...${RESET}"
}

print_success() {
    echo -e "${BOLD}${GREEN}[+] $1${RESET}"
}

print_warning() {
    echo -e "${BOLD}${YELLOW}[!] $1${RESET}"
}

print_error() {
    echo -e "${BOLD}${RED}[X] $1${RESET}"
}

# Main Execution Process
print_ascii_banner

# Verify and Enter Target Directory
print_status "Navigating to target directory: $TARGET_DIR"

if [ -d "$TARGET_DIR" ]; then
    cd "$TARGET_DIR" || { print_error "Failed to enter directory: $TARGET_DIR"; exit 1; }
    print_success "Successfully changed directory to $(pwd)"
else
    print_error "ERROR: Target directory not found at $TARGET_DIR"
    exit 1
fi

# Create Subdirectories Using Absolute Path References
print_status "Verifying required target subdirectories"

for folder in "${TARGET_FOLDERS[@]}"; do
    # Target path anchored to TARGET_DIR explicitly
    full_path="$TARGET_DIR/$folder"

    if [ ! -d "$full_path" ]; then
        if mkdir -p "$full_path"; then
            print_success "Created directory: $full_path"
        else
            print_error "Failed to create directory: $full_path"
            exit 1
        fi
    else
        print_success "Directory already exists: $full_path"
    fi
done

# 3. Processing
echo -e "${CYAN}=====================================================${RESET}"
echo -e "${RESET}${CYAN}        Sorting files into designated folders...${RESET}"
echo -e "${CYAN}=====================================================${RESET}"


# Pictures
picture_files=(*.jpg *.jpeg *.png *.gif *.svg)
if [ ${#picture_files[@]} -gt 0 ]; then
    print_status "Moving Pictures (${#picture_files[@]} found)"
    mv -vn *.jpg *.jpeg *.png *.gif *.svg Pictures/
    print_success "Pictures organized."
else
    print_warning "No picture files found to move."
fi

# Documents
document_files=(*.pdf *.doc *.docx *.txt *.pages *.csv)
if [ ${#document_files[@]} -gt 0 ]; then
    print_status "Moving Documents (${#document_files[@]} found)"
    mv -vn *.pdf *.doc *.docx *.txt *.pages *.csv Documents/
    print_success "Documents organized."
else
    print_warning "No document files found to move."
fi

# Music
music_files=(*.mp3 *.wav *.m4a *.flac)
if [ ${#music_files[@]} -gt 0 ]; then
    print_status "Moving Music files (${#music_files[@]} found)"
    mv -vn *.mp3 *.wav *.m4a *.flac Music/
    print_success "Music organized."
else
    print_warning "No music files found to move."
fi

# Videos
video_files=(*.mp4 *.mov *.avi *.mkv)
if [ ${#video_files[@]} -gt 0 ]; then
    print_status "Moving Video files (${#video_files[@]} found)"
    mv -vn *.mp4 *.mov *.avi *.mkv Videos/
    print_success "Videos organized."
else
    print_warning "No video files found to move."
fi

# Compressed Archives
archive_files=(*.zip *.tar *.gz *.rar *.7z)
if [ ${#archive_files[@]} -gt 0 ]; then
    print_status "Moving Archives (${#archive_files[@]} found)"
    mv -vn *.zip *.tar *.gz *.rar *.7z Compressed/
    print_success "Archives organized."
else
    print_warning "No archive files found to move."
fi

# disable nullglob to return shell options
shopt -u nullglob

# # 4. Completion
echo -e "${CYAN}====================================================${RESET}"
echo -e "${BOLD}${GREEN}       DOWNLOADS_CLEANBOT - EXECUTION COMPLETE       ${RESET}"
echo -e "${CYAN}====================================================${RESET}"