# Number Guesser Game

**Date:** 2026-01-08  
**Author:** omegazyph  
**Platform:** Windows 11 (Lenovo Legion)  
**Environment:** VSCode / Python 3.x  

---

## 📝 Description

The **Number Guesser** is a simple object-oriented Python application designed to manage a guessing game among multiple participants. The program generates a secret number between 1 and 10, tracks player entries, and validates whether a player is registered before accepting their guess.

## 🚀 Features

* **Automated Initialization:** Randomly generates a secret number upon game creation.
* **Player Validation:** Only allows guesses from players defined at the start of the session.
* **Status Tracking:** Distinguishes between players who have submitted a guess and those who still need to participate.
* **Modern Python Syntax:** Utilizes f-strings and PEP 8 compliant formatting for high readability.

## 🛠️ Usage

1. **Initialize the Game:** Provide a list of names to the `NumberGuesser` class.
python
    game = NumberGuesser(["Alice", "Bob", "Charlie"])

2. **Add Guesses:** Use the `add_player_guess` method.
    python
    game.add_player_guess("Alice", 5)

3. **View Results:** Call `print_guesses()` and `print_answer()` to see the outcome.

## 📂 File Structure

* `number_guesser.py`: The main Python script containing the game logic.
* `README.md`: Project documentation (this file).

## 📝 Change Log

### [2026-01-08]

* Standardized header documentation.
* Refactored code to use f-strings for better performance.
* Added logic to notify if an unregistered player attempts to guess.
* Added `if __name__ == "__main__":` guard for modularity.
