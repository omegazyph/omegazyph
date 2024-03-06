destinations = ["Paris, France", "Shanghai, China", "Los Angeles, USA", "Sao Paulo, Brazil", "Cariro, Egypt"]

test_traveler = ['Erin Wilkes', 'Shanghai, China', ['historical site', 'art']]


def get_distination_index(destination):
  destination_index = destinations.index(destination)
  return destination_index

print(get_distination_index("Los Angeles, USA"))    
