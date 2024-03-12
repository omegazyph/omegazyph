'''
inventroy of food items

shopper class
inventroy class
buget class
empolee class XXXXX
checkout class
over head class
'''

class Employee:
  def __init__(self, name, age, department):
    self.name = name
    self.age = age
    self.department = department

  def working(self):
    # Calls its method .getName()
    print("{name} is {age} working in {department}".format(name = self.getName(),age = self.age , department= self.department))

  def getName(self):
    # Accesses the name variable
    return self.name
'''

bob = Employee("Bob", 36, "perishables")
bob.working()

jane = Employee("Jane", 18, "Deli")
jane.working()
'''