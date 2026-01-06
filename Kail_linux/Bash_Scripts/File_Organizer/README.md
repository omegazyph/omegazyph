# Downloads_CleanBot 🤖

**Author:** Omegazyph
**Date:** January 4, 2026  
**Version:** 1.0.0  

## 📝 Description

`Downloads_CleanBot.sh` is a high-speed Bash utility designed to declutter your system. It automatically scans your **Downloads** folder and organizes scattered files into neat, categorized subdirectories based on their file extensions.

---

## 🚀 How It Works

The script identifies files and moves them into the following structure:

| Folder | File Types Handled |
| :--- | :--- |
| **Pictures** | .jpg, .jpeg, .png, .gif, .svg |
| **Documents** | .pdf, .doc, .docx, .txt, .pages, .csv |
| **Music** | .mp3, .wav, .m4a, .flac |
| **Videos** | .mp4, .mov, .avi, .mkv |
| **Compressed** | .zip, .tar, .gz, .rar, .7z |

---

## 🛠️ Installation & Usage

1. **Make the script executable:**
Bash
   chmod +x Downloads_CleanBot.sh

    Run the program:
    Bash

    ./Downloads_CleanBot.sh

## 🛡️ Safety Features

    Directory Verification: The script confirms the existence of the Downloads folder before running to prevent accidental file moves.

    Silent Error Handling: Uses 2>/dev/null to ensure the terminal remains clean even if certain file types aren't found.

    Verbose Reporting: Uses the -v flag so you can see exactly which files are being relocated in real-time.

## 📅 Version History

    v1.0.0 (Jan 4, 2026): Initial release. Added core sorting logic and color-coded terminal output.
