#!/usr/bin/env python3
"""
==============================================================================
SCRIPT NAME:    quiz_game.py
DESCRIPTION:    A terminal-based computer hardware quiz that tracks scores, 
                saves high scores, and copies results to the clipboard.
AUTHOR:         omegazyph
DATE CREATED:   05-22-2025
DATE UPDATED:   2026-01-05
VERSION:        1.1
==============================================================================
"""

import tkinter as tk  # Used for clipboard functionality

def copy_to_clipboard(text):
    """Copies the game results to the system clipboard using Tkinter."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()  # Stay in clipboard after window is closed
    root.destroy()
    print("\n📋 Results copied to clipboard!")

def save_high_score(score):
    """Saves the highest score achieved to a local file."""
    high_score = 0
    try:
        with open("quiz_score.txt", "r") as f:
            high_score = int(f.read().strip())
    except (FileNotFoundError, ValueError):
        high_score = 0

    if score > high_score:
        with open("quiz_score.txt", "w") as f:
            f.write(str(score))
        print(f"🏆 NEW RECORD! Your new high score is {score}.")
    else:
        print(f"High Score to beat: {high_score}")

def main():
    """Main game logic for the Quiz."""
    print("====================================")
    print("      OMEGAZYPH COMPUTER QUIZ")
    print("====================================\n")

    # Asking if the player wants to play
    playing = input("Do you want to play? (yes/no): ").lower()

    # Checking player intent
    if playing != "yes":
        print("Maybe next time! Goodbye.")
        return

    print("Okay! Let's play :)\n")
    score = 0  # Initialize score

    # Define questions and answers in a list for cleaner logic
    questions = [
        ("What does CPU stand for? ", "central processing unit"),
        ("What does GPU stand for? ", "graphics processing unit"),
        ("What does RAM stand for? ", "random access memory"),
        ("What does PSU stand for? ", "power supply")
    ]

    # Loop through questions
    for q_text, q_answer in questions:
        answer = input(q_text)
        if answer.lower() == q_answer:
            print("✅ Correct!")
            score += 1
        else:
            print("❌ Incorrect!")

    # Calculate percentages
    percent = (score / len(questions)) * 100

    # Display final results
    print("\n" + "="*30)
    print(f"FINAL SCORE: {score} / {len(questions)}")
    print(f"PERCENTAGE:  {percent}%")
    print("="*30)

    # Save high score and copy to clipboard
    save_high_score(score)
    result_text = f"I scored {score}/{len(questions)} on Omegazyph's Computer Quiz!"
    copy_to_clipboard(result_text)

if __name__ == "__main__":
    main()