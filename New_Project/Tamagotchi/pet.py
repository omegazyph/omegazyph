##########################################################################
# Date: 2026-01-09
# Script Name: pet.py
# Author: omegazyph
# Updated: 2026-01-09
# Description: A logic-based virtual pet (Tamagotchi clone) 
# that tracks hunger, happiness, and health.
#########################################################################
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
        if self.hunger > 80:
            print(f"Mood: {self.name} is starving! 🦴")
        elif self.happiness < 20:
            print(f"Mood: {self.name} is feeling lonely... ☁️")
        else:
            print(f"Mood: {self.name} is doing great! ✨")
        print("-----------------------\n")

    def pet_me(self):
        """Increases happiness but slightly increases hunger."""
        if not self.is_alive:
            print(f"Internal Error: {self.name} is not responding...")
            return

        print(f"You pet {self.name}. They look so happy!")
        self.happiness += 20
        self.hunger += 5  # Playing makes them a tiny bit hungrier
        
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

            
'''
##########################################################################
# testing 
# Create the pet
my_pet = VirtualPet("Buddy")

# Check status, feed it, then check again
my_pet.status()
my_pet.feed()
my_pet.status()
my_pet.pet_me()
my_pet.status()
#########################################################################
'''