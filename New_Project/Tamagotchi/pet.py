# Date: 2026-01-09
# Script Name: pet.py
# Author: omegazyph
# Updated: 2026-01-09
# Description: A logic-based virtual pet (Tamagotchi clone) 
# that tracks hunger, happiness, and health.

class VirtualPet:
    def __init__(self, name):
        # The name the user gives the pet
        self.name = name
        
        # 0 is full, 100 is starving
        self.hunger = 50
        
        # 100 is happy, 0 is sad
        self.happiness = 50
        
        # We track if the pet is still alive/active
        self.is_alive = True
        
        print(f"Aww! {self.name} has been born!")

    def feed(self):
        """Reduces hunger and slightly increases happiness."""
        print(f"You fed {self.name}!")
        self.hunger -= 20
        
        # Safety check: Hunger shouldn't be negative
        if self.hunger < 0:
            self.hunger = 0
            
        self.happiness += 5

    def status(self):
        """Displays the pet's current stats and mood."""
        print(f"\n--- {self.name}'s Status ---")
        print(f"Hunger: {self.hunger}/100")
        print(f"Happiness: {self.happiness}/100")
        
        # Simple mood logic based on stats
        if self.hunger > 70:
            print(f"Mood: {self.name} is starving! 🦴")
        elif self.happiness < 20:
            print(f"Mood: {self.name} is feeling lonely... ☁️")
        else:
            print(f"Mood: {self.name} is doing great! ✨")
        print("-----------------------\n")

