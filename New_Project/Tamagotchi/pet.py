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