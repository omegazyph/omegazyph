#!/bin/bash

# ==========================================================
# SCRIPT NAME:  Downloads_CleanBot.sh
# AUTHOR:       Wayne
# DATE:         January 4, 2026
# VERSION:      v1.0.0
# DESCRIPTION:  A system utility to automatically organize 
#               the Downloads folder by file extension.
# ==========================================================

# --- SETTINGS ---
TARGET_DIR="$HOME/Downloads"

# --- INITIALIZATION ---
echo -e "\033[0;36m" # Set color to Cyan
echo "===================================================="
echo "      DOWNLOADS_CLEANBOT $VERSION - INITIATED       "
echo "===================================================="
echo -e "\033[0m" # Reset color

# 1. Verify Directory
if [ -d "$TARGET_DIR" ]; then
    cd "$TARGET_DIR" || exit
else
    echo "ERROR: Target directory not found at $TARGET_DIR"
    exit 1
fi

# 2. Preparation
# Create folders (silent if they already exist)
mkdir -p Pictures Documents Music Videos Compressed

# 3. Processing
echo "Sorting files into designated folders..."
echo "----------------------------------------------------"

# Pictures
mv -v *.jpg *.jpeg *.png *.gif *.svg Pictures/ 2>/dev/null

# Documents
mv -v *.pdf *.doc *.docx *.txt *.pages *.csv Documents/ 2>/dev/null

# Music
mv -v *.mp3 *.wav *.m4a *.flac Music/ 2>/dev/null

# Videos
mv -v *.mp4 *.mov *.avi *.mkv Videos/ 2>/dev/null

# Archives/Compressed
mv -v *.zip *.tar *.gz *.rar *.7z Compressed/ 2>/dev/null

# 4. Completion
echo "----------------------------------------------------"
echo -e "\033[0;32mDONE: v1.0.0 Execution Successful.\033[0m"
echo "===================================================="