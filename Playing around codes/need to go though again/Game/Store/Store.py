"""
Store Management System
-----------------------
This script manages different entities within a grocery store,
including Employees and Shoppers, with logic for age verification.

by Omegazyph
Created 2024-03-12
Updated 2025-12-25
"""

class Employee:
    """Represents a staff member working at the store."""
    
    def __init__(self, name, age, department):
        self.name = name
        self.age = age
        self.department = department

    def working(self):
        """Prints a status message about the employee's current work."""
        # Fixed the variable name from namgite to name
        print("{name} is {age} and currently working in {department}.".format(
            name=self.name, 
            age=self.age, 
            department=self.department
        ))
    
    def __repr__(self):
        """Returns a string representation of the employee object."""
        return "Employee: {name} | Dept: {department} | Age: {age}".format(
            name=self.name, 
            department=self.department, 
            age=self.age
        )


class Shopper:
    """Represents a customer visiting the store."""
    
    def __init__(self, input_name, input_age, has_id):
        self.name = input_name
        self.age = input_age
        self.has_id = has_id # renamed from id to has_id for clarity

    def id_check(self):
        """Initial check to see if the customer even has an ID card."""
        if self.has_id:
            self.check_age()  
        else:
            print("{name} cannot buy cigarettes (No ID provided).".format(name=self.name))

    def check_age(self):
        """Verifies if the customer meets the legal age requirement (21)."""
        minimum_age = 21
        if self.age >= minimum_age:
            print("{name} is old enough to buy cigarettes.".format(name=self.name))
        else:
            # Added a more specific message for being underage
            print("{name} is only {age}; they are too young.".format(
                name=self.name, 
                age=self.age
            ))

    def __repr__(self):
        """Returns a string summary of the shopper."""
        return "Customer: {name} (Age: {age}, Has ID: {has_id})".format(
            name=self.name, 
            age=self.age, 
            has_id=self.has_id
        )

# --- Execution / Testing Section ---

# Employee Data
bob = Employee("Bob", 36, "perishables")
jane = Employee("Jane", 18, "Deli")

print("--- Employee Info ---")
print(bob)
bob.working()
print(jane)
jane.working()

print("\n--- Shopper Info ---")
# Shopper Data
richard = Shopper("Richard", 21, True)
mary = Shopper("Mary", 12, False)

print(richard)
richard.id_check()

print(mary)
mary.id_check()