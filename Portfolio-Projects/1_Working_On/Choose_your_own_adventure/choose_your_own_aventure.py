#!/usr/bin/env python3
"""
==============================================================================
SCRIPT NAME:    choose_your_own_aventure.py
DESCRIPTION:    A text-based adventure game with branching paths, name tracking,
                and clipboard result sharing.
AUTHOR:         Wayne Stock (omegazyph)
DATE CREATED:   2024-04-23
DATE UPDATED:   2026-01-05
VERSION:        1.1
==============================================================================
"""

import tkinter as tk

def copy_to_clipboard(text):
    """Utility to copy the final game result to the clipboard."""
    root = tk.Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()
    root.destroy()
    print("\n📋 Your adventure outcome has been copied to the clipboard!")

def main():
    """Main game logic for the adventure."""
    # Getting player name
    name = input("Type your name :> ").strip()
    if not name:
        name = "Adventurer"
        
    print(f"Welcome {name} to this adventure!")
    ending = ""

    # Path Choice 1: The Dirt Road
    answer = input("You are on a dirt road, it has come to an end and you can go left or right. "
                   "Which way would you like to go? :> ").lower()

    if answer == "left":
        # Path 2: The River
        answer = input("You come to a river, you can walk around it or swim across? "
                       "Type walk or swim :> ").lower()
        
        if answer == "swim":
            print("You swam across and were eaten by an alligator.")
            ending = "Eaten by an alligator"
        elif answer == "walk":
            print("You walked for many miles, ran out of water and you lost the game.")
            ending = "Ran out of water"
        else:
            print("Not a valid option. You lose.")
            ending = "Indecision"

    elif answer == "right":
        # Path 2: The Bridge
        answer = input("You come to a bridge, it looks wobbly, do you want to cross it, "
                       "or head back? (cross/back) :> ").lower()
        
        if answer == "back":
            print("You go back and lose.")
            ending = "Turned back too soon"
        elif answer == "cross":
            # Path 3: The Stranger
            answer = input("You cross the bridge and meet a stranger. "
                           "Do you talk to them (yes/no)? :> ").lower()
            
            if answer == "yes":
                print("You talked to the stranger and they give you gold. You WIN!")
                ending = "The Golden Winner"
            elif answer == "no":
                print("You ignore the stranger and they were offended and you lose.")
                ending = "Offended the Stranger"
            else:
                print("Not a valid option. You lose.")
                ending = "Lost your way"
        else:
            print("Not a valid option. You lose.")
            ending = "Bridge Accident"
    else:
        print("Not a valid option. You lose.")
        ending = "Stayed at the start"

    # Closing message
    print(f"\nThank you for trying, {name}")
    
    # Copying the result to the clipboard
    if ending:
        summary = f"{name} played Omegazyph's Adventure and reached this end: {ending}!"
        copy_to_clipboard(summary)

if __name__ == "__main__":
    main()