# 🗺️ Choose Your Own Adventure (v1.1)

## 📝 Overview

**Choose Your Own Adventure** is a text-based narrative engine created by **Wayne Stock (omegazyph)**. It puts the player in control of a high-stakes journey where every decision—from choosing a path on a dirt road to interacting with strangers—determines whether they find gold or meet a sudden end.

## ✨ Current Features

* **Dynamic Storytelling:** Multiple branching paths with unique outcomes.
* **Player Personalization:** Tracks and greets the user by name.
* **Clipboard Integration:** Automatically copies the specific ending reached to the clipboard for easy sharing.
* **Robust Input Handling:** Uses case-insensitive matching to ensure a smooth player experience.

## 📂 File Structure

* `choose_your_own_aventure.py`: The main game logic and story data.
* `README.md`: Project documentation and roadmap.

## 🚀 How to Play

1. **Launch the Game:**

'''bash
    python3 choose_your_own_aventure.py
    '''
2. **Input Your Name:** This will be used to track your progress and results.
3. **Make Choices:** Type your decisions (e.g., `left`, `right`, `swim`, `talk`) exactly as prompted.
4. **Share Your Ending:** Once the game ends, your outcome is already on your clipboard! Just `Ctrl+V` to share it.

## 🛠️ Future Roadmap

As the project evolves, the following features are planned for implementation:

* [ ] **Inventory System:** Allow players to pick up items (like a "Map" or "Water") that unlock new paths.
* [ ] **Health Points (HP):** Instead of instant death, some choices will reduce health.
* [ ] **Save States:** The ability to save your progress and return to a specific "checkpoint."
* [ ] **Random Encounters:** Add a layer of unpredictability using the `random` library.

---
**Developer:** Wayne Stock (omegazyph)  
**Version:** 1.1  
**Updated:** 2026-01-05
