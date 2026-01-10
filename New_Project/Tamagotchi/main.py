##########################################################################
# Date: 2026-01-09
# Script Name: main.py
# Author: omegazyph
# Updated: 2026-01-10
# Description: The main game loop and terminal interface for the Pet.
##########################################################################

import os
from pet_logic import VirtualPet

def main():
    # 1. Setup: Try to load an existing pet FIRST
    # We use the class method we added to pet_logic.py
    my_pet = VirtualPet.load_pet()

    if my_pet:
        print(f"Welcome back! {my_pet.name} was waiting for you.")
        input("Press Enter to continue...")
    else:
        # No save file found, only then do we ask for a name
        print("No save found.")
        pet_name = input("What would you like to name your new pet? ")
        my_pet = VirtualPet(pet_name)

    # 2. The Game Loop
    while my_pet.is_alive:
        # Clear terminal for Windows 11
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
            # Save the pet's progress to the JSON file before closing
            my_pet.save_pet()
            print("\nProgress saved. Thanks for playing!")
            break
        else:
            print("Invalid action. Try again.")

        # Every action (except quit) makes time pass slightly
        if choice != "quit":
            my_pet.pass_time()
            my_pet.check_vitals()
            # Pause so the user can read any warnings before the screen clears
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
    