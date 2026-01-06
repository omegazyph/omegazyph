#!/usr/bin/env python3
"""
==============================================================================
SCRIPT NAME:    quiz_game.py
DESCRIPTION:    A terminal-based computer hardware quiz with name tracking,
                persistent high scores, and clipboard support.
AUTHOR:         omegazyph
DATE CREATED:   05-22-2025
DATE UPDATED:   2026-01-05
VERSION:        1.2
==============================================================================
"""

import tkinter as tk  # Import for clipboard functionality

def copy_to_clipboard(text):
    """Copies the game results to the system clipboard."""
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()  # Required to keep text in clipboard after destroy
    root.destroy()
    print("\n📋 Results copied to clipboard!")

def save_high_score(name, score):
    """Saves the highest score and the player's name to quiz_score.txt."""
    high_score = 0
    try:
        with open("quiz_score.txt", "r") as f:
            content = f.read().strip()
            if ":" in content:
                # Split 'Name:Score' to compare the integer value
                high_score = int(content.split(":")[1])
    except (FileNotFoundError, ValueError, IndexError):
        high_score = 0

    # Only update if the new score is strictly better than the old record
    if score > high_score:
        with open("quiz_score.txt", "w") as f:
            f.write(f"{name}:{score}")
        print(f"🏆 NEW RECORD! {name} now holds the top spot with {score} points.")
    else:
        print(f"Current record holder has {high_score} points.")

def main():
    """Main game logic including name input and hardware questions."""
    print("====================================")
    print("      OMEGAZYPH COMPUTER QUIZ")
    print("====================================\n")

    # Ask for player identity
    player_name = input("Enter your name: ").strip()
    if not player_name:
        player_name = "Player 1"

    # Verify if player wants to begin
    playing = input(f"Hello {player_name}, do you want to play? (yes/no): ").lower()
    if playing != "yes":
        print("Goodbye!")
        return

    print("Okay! Let's play :)\n")
    score = 0

    # Question bank stored in a list of tuples (Question, Answer)
    questions = [
        ("What does CPU stand for? ", "central processing unit"),
        ("What does GPU stand for? ", "graphics processing unit"),
        ("What does RAM stand for? ", "random access memory"),
        ("What does PSU stand for? ", "power supply")
    ]

    # Iterate through questions and validate input
    for q_text, q_answer in questions:
        answer = input(q_text)
        if answer.lower() == q_answer:
            print("✅ Correct!")
            score += 1
        else:
            print("❌ Incorrect!")

    # Calculate final stats
    percent = (score / len(questions)) * 100

    print("\n" + "="*30)
    print(f"PLAYER:      {player_name}")
    print(f"FINAL SCORE: {score} / {len(questions)}")
    print(f"PERCENTAGE:  {percent}%")
    print("="*30)

    # Persist the score and copy summary to clipboard
    save_high_score(player_name, score)
    result_text = f"{player_name} scored {score}/{len(questions)} on Omegazyph's Quiz!"
    copy_to_clipboard(result_text)

if __name__ == "__main__":
    main()