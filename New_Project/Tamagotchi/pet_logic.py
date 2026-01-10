##########################################################################
# Date: 2026-01-09
# Script Name: pet_logic.py
# Author: omegazyph
# Updated: 2026-01-10
# Description: Contains the VirtualPet class logic, stats, and visuals.
##########################################################################

class VirtualPet:
    def __init__(self, name):
        self.name = name
        self.hunger = 50
        self.happiness = 50
        self.health = 100
        self.level = 1
        self.experience = 0
        self.is_alive = True
        print(f"Aww! {self.name} has been born!")

    def feed(self):
        """Reduces hunger and slightly increases happiness."""
        print(f"\nYou fed {self.name}!")
        self.hunger -= 20
        self.gain_xp(20)
        if self.hunger < 0:
            self.hunger = 0
        self.happiness += 5

    def status(self):
        """Displays the pet's visual appearance and stats."""
        print("\n" + "="*20)
        print(self.get_visual())
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
        self.hunger += 5
        self.gain_xp(10)
        
        if self.happiness > 100:
            self.happiness = 100

    def pass_time(self):
        """Simulates the passage of time. Stats decay naturally."""
        self.hunger += 10
        self.happiness -= 5
        if self.hunger >= 100:
            self.hunger = 100
        if self.happiness <= 0:
            self.happiness = 0

    def check_vitals(self):
        """Checks if the pet is sick or has passed away."""
        if self.hunger >= 100:
            self.health -= 20
            print(f"⚠️ {self.name} is starving and losing health!")
        if self.happiness <= 0:
            self.health -= 5
            print(f"⚠️ {self.name} is depressed and losing health!")
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
        return "   (^_^) \n    /| \\\n   / |  \\"
    
    def gain_xp(self, amount):
        """Adds XP and checks for a level up."""
        self.experience += amount
        if self.experience >= (self.level * 100):
            self.level += 1
            self.experience = 0
            print(f"✨ LEVEL UP! {self.name} is now Level {self.level}! ✨")
            self.health = 100