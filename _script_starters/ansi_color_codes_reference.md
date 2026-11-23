# ANSI Color Codes Reference

## Standard Foreground Colors (`30`–`37`)

| Color Name | Normal (`0;...m`) | Bold (`1;...m`) |
| :--- | :--- | :--- |
| **Black** | `"\033[0;30m"` | `"\033[1;30m"` |
| **Red** | `"\033[0;31m"` | `"\033[1;31m"` |
| **Green** | `"\033[0;32m"` | `"\033[1;32m"` |
| **Yellow** | `"\033[0;33m"` | `"\033[1;33m"` |
| **Blue** | `"\033[0;34m"` | `"\033[1;34m"` |
| **Magenta / Purple** | `"\033[0;35m"` | `"\033[1;35m"` |
| **Cyan** | `"\033[0;36m"` | `"\033[1;36m"` |
| **White** | `"\033[0;37m"` | `"\033[1;37m"` |

## Bright Foreground Colors (`90`–`97`)

| Color Name | Bright (`0;9Xm` / `9Xm`) | Bold + Bright (`1;9Xm`) |
| :--- | :--- | :--- |
| **Bright Black (Gray)** | `"\033[0;90m"` | `"\033[1;90m"` |
| **Bright Red** | `"\033[0;91m"` | `"\033[1;91m"` |
| **Bright Green** | `"\033[0;92m"` | `"\033[1;92m"` |
| **Bright Yellow** | `"\033[0;93m"` | `"\033[1;93m"` |
| **Bright Blue** | `"\033[0;94m"` | `"\033[1;94m"` |
| **Bright Magenta** | `"\033[0;95m"` | `"\033[1;95m"` |
| **Bright Cyan** | `"\033[0;96m"` | `"\033[1;96m"` |
| **Bright White** | `"\033[0;97m"` | `"\033[1;97m"` |

## Background Colors & Reset (`40`–`47` / `100`–`107`)

* **Reset all formatting:** `"\033[0m"`
* **Standard backgrounds (`40`–`47`):** Black `40`, Red `41`, Green `42`, Yellow `43`, Blue `44`, Magenta `45`, Cyan `46`, White `47` (for example, `"\033[41m"`).
* **Bright backgrounds (`100`–`107`):** High-intensity versions of the eight background colors (`100` through `107`).

## 256-Color (8-Bit) and Truecolor (24-Bit RGB)

* **256-color foreground:** `"\033[38;5;{ID}m"` where `{ID}` is `0`–`255` (`0–7` basic, `8–15` bright, `16–231` 6x6x6 color cube, `232–255` grayscale steps).
* **256-color background:** `"\033[48;5;{ID}m"` where `{ID}` is `0`–`255`.
* **24-bit RGB foreground:** `"\033[38;2;{R};{G};{B}m"` with each channel from `0` to `255` (for example, `"\033[38;2;255;82;197m"`).
* **24-bit RGB background:** `"\033[48;2;{R};{G};{B}m"` with each channel from `0` to `255`.