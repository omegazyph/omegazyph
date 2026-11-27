# ASCII Art Banner Generator (`ascii_art1_3.py`)

An interactive command-line Python script that renders custom ASCII art banners using `pyfiglet`, featuring a startup logo, typewriter-style ANSI color output, an expanded 10-font menu, and a loop that lets you preview multiple fonts with the same banner text.

## Project Structure

```text
ascii_art_project/
├── ascii_art1_3.py
└── README.md
```

## Features

- **Startup Logo & Dynamic Banners:** Displays the Omegazyph ASCII logo and centered border banners (`print_logo` and `print_ascii_banner`).
- **Typewriter Output & ANSI Colors:** Prints UI messages and banners with character-by-character timing and bold ANSI color codes.
- **Persistent Banner Text:** Prompts for your banner text once before entering the font-selection loop so you can test multiple styles without re-typing your phrase.
- **10 Font Choices:** Choose from `Slant`, `Standard`, `3D Banner`, `Block`, `Digital`, `Big`, `Doom`, `Larry 3D`, `Rectangles`, and `Small` (with automatic fallback to `slant` for invalid choices or missing fonts).
- **Graceful Exit Handling:** Handles `Ctrl+C` (`KeyboardInterrupt`) cleanly and prints a closing banner when finished.

## Requirements

- Python 3.x
- `pyfiglet`

Install `pyfiglet` using `pip`:

```bash
pip install pyfiglet
```

## Usage

Run the script from your terminal or VS Code:

```bash
python ascii_art1_3.py
```

1. Enter the text you want turned into an ASCII banner.
2. Pick a font number from `1` to `10`.
3. View the generated banner, then choose `y` to try another font with the same text or `n` to exit.