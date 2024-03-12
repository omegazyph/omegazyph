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
    print("{name} is {age} working in {department}".format(name = self.name,age = self.age , department= self.department))
  
  def __repr__(self):
    return "I have {name} woking in {department} that is {age} years old".format(name = self.name, department = self.department, age = self.age)
'''#Employee info
bob = Employee("Bob", 36, "perishables")
print(repr(bob))
bob.working()


jane = Employee("Jane", 18, "Deli")
print(repr(jane))
jane.working()
'''


class Shopper:
  def __init__(self,input_name, input_age, input_ID):
    self.name = input_name
    self.age = input_age
    self.id = input_ID

  def id_check(self):
    if self.id == True:
      self.check_age()  
    else:
       print("{name} is NOT old enough to buy cigerttes".format(name = self.name))

  def check_age(self):
    minimum_age = 21

    if self.age >= minimum_age:
      print("{name} is old enough to buy cigerttes".format(name = self.name))
    else:
     print("somthing is wrong")

  def __repr__(self):
    return " The customer {name} is {age} and has id {id}.".format(name = self.name, age = self.age, id = self.id)
#shopper info
richard = Shopper("Richard", 21, True)
print(repr(richard))
#richard.id_check()

mary = Shopper("Mary", 12, False)
print(repr(mary))
#mary.id_check()