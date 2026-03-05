# Gate Keeper Security Suite

**Gate Keeper** is a clever, lightweight JavaScript security system that uses a "Filename-as-Password" logic. Instead of hardcoding passwords, the password *is* the name of the file you are trying to access.

## 🚀 How It Works

1. **The Entrance:** Users start at `index.html`.
2. **The Popup:** A centered, 350x200 security window appears.
3. **The Challenge:** The user enters a password (e.g., `mypage`).
4. **The Gopher:** The script looks for a file named `mypage.html`. If it exists, the main window redirects there.

## 📂 Project Structure

* **index.html** — The main entry point.
* **gatekeep.html** — The security challenge popup.
* **/JavaScripts/** — Contains the logic for launching windows and fetching files.
* **Notes.txt** — Original development notes and logic rules.

## 🛠️ Implementation Details

To protect a new page, simply rename your HTML file to a complex string. That string becomes the password.

> **Note:** This system specifically requires the `.html` extension. It will not recognize `.htm` files.

## 🔒 Security Advantages

* **No Hardcoded Passwords:** No one can find the password by "viewing source" on your JavaScript.
* **Easy Updates:** To change a password, just rename the file on the server.
* **Zero-Footprint:** You don't have to add any extra code to the pages you are protecting.
