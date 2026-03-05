# 🧩 Homophonic Cipher Suite

A Python-based cryptographic toolset designed to demonstrate homophonic substitution. This method maps single plaintext characters to multiple ciphertext symbols to defeat frequency analysis, similar to historical ciphers like the Zodiac 340.

## 📂 Project Structure

### ⚙️ Core Programs

* **`cipher_program.py`**: The main interactive controller for quick encoding/decoding in the terminal.
* **`cipher_io.py`**: A file management utility to process bulk data from `.txt` files with auto-wrapping features.
* **`encode.py`**: The logic module responsible for random symbol selection.
* **`decode.py`**: The logic module that uses a reverse-pointer map to reconstruct messages.

### 📝 Data Files

* **`cipher_map.json`**: The central key containing the one-to-many character mappings.
* **`plaintext.txt`**: The original secret message (the starting point).
* **`ciphertext.txt`**: The encrypted output, formatted into 50-character blocks for readability.
* **`decrypted.txt`**: The final result after running the decoder, used for verification.

## 🚀 Usage

### Interactive Mode

To encode or decode messages directly in your terminal, run:

```bash
python cipher_program.py
