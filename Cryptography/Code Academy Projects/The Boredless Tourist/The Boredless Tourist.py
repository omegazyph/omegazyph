# Define a list of destinations
destinations = ["Paris, France", "Shanghai, China", "Los Angeles, USA", "Sao Paulo, Brazil", "Cairo, Egypt"]

# Define a test traveler with name, destination, and list of interests
test_traveler = ['Erin Wilkes', 'Shanghai, China', ['historical site', 'art']]



# Define a function to get the index of a destination in the destinations list
def get_destination_index(destination):
    # Use the index method to find the index of the destination in the list
    try:
        destination_index = destinations.index(destination)
        return destination_index
    # Handle the case when the destination is not found in the list
    except ValueError:
        print("Destination not found in the list")
        return None



# Test the function with different destinations
print(get_destination_index("Los Angeles, USA"))  # Output: 2 (index of "Los Angeles, USA" in the list)
print(get_destination_index("Paris, France"))    # Output: 0 (index of "Paris, France" in the list)
print(get_destination_index("Hyderabad, India")) # Output: None (destination not found)
