# Define a list of destinations
destinations = ["Paris, France", "Shanghai, China", "Los Angeles, USA", "Sao Paulo, Brazil", "Cairo, Egypt"]

# Define a test traveler with name, destination, and list of interests
test_traveler = ['Erin Wilkes', 'Shanghai, China', ['historical site', 'art']]



# Define a function to get the index of a destination in the destinations list
def get_destination_index(destination):
    destination_index = destinations.index(destination)
    return destination_index
    