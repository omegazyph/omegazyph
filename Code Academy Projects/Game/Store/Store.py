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
''' Employee info


bob = Employee("Bob", 36, "perishables")
bob.working()

jane = Employee("Jane", 18, "Deli")
jane.working()
'''

class Shopper:
  def __init__(self,input_name, input_age):
    self.name = input_name
    self.age = input_age

  def check_age(self):
    minimum_age = 21

    if self.age >= minimum_age:
      print("{name} is old enough to buy cigerttes".format(name = self.getName()))
    else:
      print("{name} is NOT old enough to buy cigerttes".format(name = self.getName()))

  def getName(self):
    return self.name
'''shopper info
richard = Shopper("Richard", 21)
richard.check_age()

mary = Shopper("Mary", 12)
mary.check_age()
'''