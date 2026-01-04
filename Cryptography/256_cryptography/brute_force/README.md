# Tool 2: Hash Cracker (Hash_Cracker_v1.sh)

The cracker script is designed to be "bulletproof" against common formatting errors that cause other simple scripts to fail.

## Key Features

* **Dual-State Verification**: It automatically checks for hashes generated both with and without trailing newlines. This solves the most common "No Match" error in Bash scripting.
* **Character Sanitization**: It strips away `\r` (Windows Carriage Returns) and leading/trailing whitespace using `tr` and `xargs`.
* **Last-Line Safety**: It uses specialized logic to ensure the very last word in your password list is checked, even if the file doesn't end in a blank line.

### Comparison Logic

The script performs the following logic internally for every word in your list:

1. **Input:** `123456`

2. **Test A:** `echo "123456" | sha256sum` (Standard Linux output)
3. **Test B:** `printf "123456" | sha256sum` (Standard Web/Programming output)
4. **Match:** If either result matches `inputhash.txt`, the script succeeds.
