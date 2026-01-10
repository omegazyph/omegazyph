##########################################################################
# Date: 2026-01-10
# Script Name: main.py
# Author: omegazyph
# Updated: 2026-01-10
# Description: The main game loop and terminal interface for the Pet.
##########################################################################

import os
from pet_logic import VirtualPet  # This imports your class from the other file

def main():
    # 1. Setup: Ask for the pet's name
    pet_name = input("What would you like to name your pet? ")
    my_pet = VirtualPet(pet_name)

    # 2. The Game Loop
    while my_pet.is_alive:
        # Clear terminal for Lenovo/Windows 11
        os.system('cls' if os.name == 'nt' else 'clear')

        my_pet.status()
        
        # Get user input
        print("Actions: [feed] [pet] [wait] [quit]\n")
        choice = input(f"What will you do with {my_pet.name}? ").lower().strip()

        # 3. Handle the choices
        if choice == "feed":
            my_pet.feed()
        elif choice == "pet":
            my_pet.pet_me()
        elif choice == "wait":
            print(f"\nYou watch {my_pet.name} play for a bit.")
        elif choice == "quit":
            print("\nThanks for playing!")
            break
        else:
            print("Invalid action. Try again.")

        # Every action (except quit) makes time pass slightly
        if choice != "quit":
            my_pet.pass_time()
            my_pet.check_vitals()
            # Pause so the user can read any warnings/messages before the screen clears
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()