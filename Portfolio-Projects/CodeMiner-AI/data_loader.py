def load_sample_data():
    return """
def greet(name):
    print("Hello " + name)

def add(a, b):
    return a + b

def check_even(num):
    if num % 2 == 0:
        return True
    else:
        return False

for i in range(10):
    result = add(i, 5)
    print(result)

class Robot:
    def __init__(self, name):
        self.name = name
    def say_hi(self):
        print("I am " + self.name)
"""