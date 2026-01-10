##########################################################################
# Date: 2026-01-09
# Script Name: pet.py
# Author: omegazyph
# Updated: 2026-01-09
# Description: A logic-based virtual pet (Tamagotchi clone) 
# that tracks hunger, happiness, and health.
#########################################################################

import os


class VirtualPet:
    def __init__(self, name):
        # The name the user gives the pet
        self.name = name
        
        # 0 is full, 100 is starving
        self.hunger = 50
        
        # 100 is happy, 0 is sad
        self.happiness = 50

        # 100 is healthy, 0 is dead
        self.health = 100

        self.level = 1          # Start at Level 1
        self.experience = 0     # Start with 0 XP
        
        # We track if the pet is still alive/active
        self.is_alive = True
        
        print(f"Aww! {self.name} has been born!")

    def feed(self):
        """Reduces hunger and slightly increases happiness."""
        print(f"\nYou fed {self.name}!")
        self.hunger -= 20
        self.gain_xp(20) # Reward 20 XP for feeding
        
        # Safety check: Hunger shouldn't be negative
        if self.hunger < 0:
            self.hunger = 0
            
        self.happiness += 5

    def status(self):
        """Displays the pet's visual appearance and stats."""
        print("\n" + "="*20)
        print(self.get_visual()) # This calls our new ASCII function
        print("="*20)
        print(f"Name:      {self.name}")
        print(f"Level:     {self.level} (XP: {self.experience}/{self.level * 100})")
        print(f"Health:    {self.health}/100")
        print(f"Hunger:    {self.hunger}/100")
        print(f"Happiness: {self.happiness}/100")
        print("="*20 + "\n")

    def pet_me(self):
        """Increases happiness but slightly increases hunger."""
        if not self.is_alive:
            print(f"Internal Error: {self.name} is not responding...")
            return

        print(f"\nYou pet {self.name}. They look so happy!")
        self.happiness += 20
        self.hunger += 5  # Playing makes them a tiny bit hungrier
        self.gain_xp(10) # Reward 10 XP for petting
        
        # Cap happiness at 100
        if self.happiness > 100:
            self.happiness = 100
            print(f"{self.name} is as happy as can be!")

    def pass_time(self):

        """Simulates the passage of time. Stats decay naturally."""
        self.hunger += 10
        self.happiness -= 5
        
        # Check if the pet has been neglected for too long
        if self.hunger >= 100:
            self.hunger = 100
            print(f"Warning: {self.name} is extremely hungry!")
            
        if self.happiness <= 0:
            self.happiness = 0
            print(f"Warning: {self.name} is very sad.")

    def check_vitals(self):
        """Checks if the pet is sick or has passed away."""
        # If hunger is maxed out, health starts to drop
        if self.hunger >= 100:
            self.health -= 20
            print(f"⚠️ {self.name} is starving and losing health!")

        # If happiness is zero, health drops slowly (depression)
        if self.happiness <= 0:
            self.health -= 5
            print(f"⚠️ {self.name} is depressed and losing health!")

        # Death condition
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
            print(f"💀 Oh no! {self.name} has passed away...")

    def get_visual(self):
        """Returns an ASCII representation of the pet based on its state."""
        if not self.is_alive:
            return "   (x_x)\n    /| \\\n   / |  \\"
        
        if self.health < 30:
            return "   (o_o) <( I don't feel good...)\n    /| \\\n   / |  \\"
        
        if self.hunger > 70:
            return "   (Q_Q) <( So hungry...)\n    /| \\\n   / |  \\"
            
        if self.happiness > 80:
            return "   (^▽^) <( I love you!)\n    /| \\\n   / |  \\"
            
        # Default happy state
        return "   (^_^) \n    /| \\\n   / |  \\"
    
    def gain_xp(self, amount):
        """Adds XP and checks for a level up."""
        self.experience += amount
        # Formula: Level up every 100 XP
        if self.experience >= (self.level * 100):
            self.level += 1
            self.experience = 0 # Reset XP for the next level
            print(f"✨ LEVEL UP! {self.name} is now Level {self.level}! ✨")
            # Maybe boost health as a reward?
            self.health = 100



def main():
    # 1. Setup: Ask for the pet's name
    pet_name = input("What would you like to name your pet? ")
    my_pet = VirtualPet(pet_name)

    # 2. The Game Loop
    while my_pet.is_alive:

        # This clears the terminal so the pet stays in the same spot
        # 'cls' is for Windows (Lenovo Legion), 'clear' is for Mac/Linux
        os.system('cls' if os.name == 'nt' else 'clear')

        my_pet.status()
        
        # Get user input
        print("Actions: [feed] [pet] [wait] [quit]\n")
        choice = input(f"What will you do with {my_pet.name}? ").lower().strip()

        # 3. Handle the choices
        if choice == "feed":
            my_pet.feed()
            print("\n")

        elif choice == "pet":
            my_pet.pet_me()
            print("\n")

        elif choice == "wait":
            print(f"\nYou watch {my_pet.name} play for a bit.")
            my_pet.pass_time()
            print("\n")

        elif choice == "quit":
            print("\nThanks for playing!")
            break
        else:
            print("Invalid action. Try again.")

        # Every action (except quit) makes time pass slightly
        if choice != "quit":
            my_pet.pass_time()
            my_pet.check_vitals()

# This tells Python to run the main function when the script starts
if __name__ == "__main__":
    main()