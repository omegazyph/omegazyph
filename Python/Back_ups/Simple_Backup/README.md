# Smart Backup Script

**Author:** omegazyph  
**Date:** 2026-01-06  
**Language:** Python 3

## 📝 Description

This is a lightweight Python automation tool designed to sync files from a source folder to a backup folder. Unlike a basic copy-paste, this script is **incremental**, meaning it only copies files that are new or have been modified since the last run.

## 🚀 Features

* **Smart Detection:** Compares "Last Modified" timestamps to avoid redundant copying.
* **Auto-Discovery:** Uses absolute paths to find folders relative to the script's location.
* **Summary Report:** Displays a count of files updated versus files skipped at the end of the process.
* **Metadata Preservation:** Uses `shutil.copy2` to keep original file creation dates.

## 📂 Folder Structure

To use this script, organize your files like this:

text
Project_Folder/
│
├── smart_backup.py      # The script
├── my_files/            # Put files you want to back up here
└── backup_folder/       # The script will create this automatically

## 🛠️ How to Use

    Setup: Create a folder named my_files in the same directory as the script.

    Add Files: Place the files you want to protect inside my_files.

    Run: Execute the script using Python:
    Bash

    python smart_backup.py

    Review: Check the console output to see which files were updated.

## 📱 Running on Android

If you are using Pydroid 3 or Termux:

    Ensure the app has Storage Permissions.

    Keep the script and the my_files folder in a location like /sdcard/Documents/
    