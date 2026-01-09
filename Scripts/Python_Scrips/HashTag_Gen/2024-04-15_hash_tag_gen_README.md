# Python Utilities Project

**Date:** 2026-01-08  
**Author:** omegazyph  
**Platform:** Windows 11 (Lenovo Legion)  
**Environment:** VSCode / Python 3.x  

---

## 📝 Overview

This project is a collection of Python utility classes designed for game management and text processing. It demonstrates object-oriented programming (OOP) principles and clean code practices.

## 🛠️ Included Utilities

### 1. Number Guesser (`NumberGuesser`)

Manages a guessing game where a random secret number is generated, and registered players can submit their guesses.

- **Key Logic:** Validates player names before accepting guesses and tracks game state.

### 2. Hashtag Creator (`HashtagsCreator`)

Processes a list of strings and converts them into properly formatted hashtags.

- **Key Logic:** Handles `@` symbol replacement and ensures every term starts with a `#`.

## 🚀 How to Run

Each utility is wrapped in a `main` guard. To use them, simply run the script in VSCode:

bash
python utility_scripts.py

## 📂 Project Structure

    utility_scripts.py: Contains both NumberGuesser and HashtagsCreator classes.

    README.md: This documentation.

## 📝 Change Log

[2026-01-08]

    Consolidated Number Guesser and Hashtag Creator into a single project.

    Applied standardized headers and f-string formatting to all classes.

    Added documentation for all methods.
    