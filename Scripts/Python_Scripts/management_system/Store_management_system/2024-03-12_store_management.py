"""
==============================================================================================
Date: 2024-03-12
Script Name: store_management.py
Author: omegazyph
Updated: 2025-12-25
Description: A Store Management System that handles Employee work status 
             and Shopper age verification for restricted items.
==============================================================================================
"""

class Employee:
    """Represents a staff member working at the store."""
    
    def __init__(self, name, age, department):
        """
        Initializes employee details.
        :param name: Employee's name
        :param age: Employee's age
        :param department: Assigned work area
        """
        self.name = name
        self.age = age
        self.department = department

    def working(self):
        """Prints a status message about the employee's current work status."""
        # Cleaned up using f-strings for VSCode readability
        print(f"{self.name} is {self.age} and currently working in {self.department}.")
    
    def __repr__(self):
        """Returns a string representation of the employee object for debugging/logging."""
        return f"Employee: {self.name} | Dept: {self.department} | Age: {self.age}"


class Shopper:
    """Represents a customer visiting the store and handles age-restricted logic."""
    
    def __init__(self, input_name, input_age, has_id):
        """
        Initializes shopper details and ID status.
        :param input_name: Customer's name
        :param input_age: Customer's age
        :param has_id: Boolean indicating if they have identification
        """
        self.name = input_name
        self.age = input_age
        self.has_id = has_id 

    def id_check(self):
        """Triggers the age check only if an ID is present."""
        if self.has_id:
            self.check_age()  
        else:
            print(f"{self.name} cannot buy cigarettes (No ID provided).")

    def check_age(self):
        """Verifies if the customer meets the legal age requirement (21)."""
        minimum_age = 21
        if self.age >= minimum_age:
            print(f"{self.name} is old enough to buy cigarettes.")
        else:
            print(f"{self.name} is only {self.age}; they are too young.")

    def __repr__(self):
        """Returns a summarized string of the shopper's details."""
        return f"Customer: {self.name} (Age: {self.age}, Has ID: {self.has_id})"

# --- Execution / Testing Section ---

if __name__ == "__main__":
    # Initialize Employee Data
    bob = Employee("Bob", 36, "perishables")
    jane = Employee("Jane", 18, "Deli")

    print("--- Employee Info ---")
    print(bob)
    bob.working()
    print(jane)
    jane.working()

    print("\n--- Shopper Info ---")
    # Initialize Shopper Data
    richard = Shopper("Richard", 21, True)
    mary = Shopper("Mary", 12, False)

    print(richard)
    richard.id_check()

    print(mary)
    mary.id_check()