# Setting up Project
destinations = ["Paris, France", "Shanghai, China", "Los Angeles, USA", "São Paulo, Brazil", "Cairo, Egypt"]

test_traveler = ['Erin Wilkes', 'Shanghai, China', ['historical site', 'art']]


# Travelling to Faraway Lands
def get_destination_index(destination):
    destination_index = destinations.index(destination)
    return destination_index


def get_traveler_location(traveler):
    traveler_destination = traveler[1]
    traveler_destination_index = get_destination_index(traveler_destination)
    return traveler_destination_index

test_destination_index = get_traveler_location(test_traveler)
#print(test_destination_index)


# Visiting Interesting Places
attractions = [[] for destination in destinations]
#print(attractions)


def add_attraction(destination, attraction):
    destination_index = get_destination_index(destination)
    attractions[destination_index].append(attraction)


add_attraction("Los Angeles, USA", ["Venice Beach", ['beach']])
add_attraction("Paris, France", ["the Louvre", ["art", "museum"]])
add_attraction("Paris, France", ["Arc de Triomphe", ["historical site", "monument"]])
add_attraction("Shanghai, China", ["Yu Garden", ["garden", "historical site"]])
add_attraction("Shanghai, China", ["Yuz Museum", ["art", "museum"]])
add_attraction("Shanghai, China", ["Oriental Pearl Tower", ["skyscraper", "viewing deck"]])
add_attraction("Los Angeles, USA", ["LACMA", ["art", "museum"]])
add_attraction("São Paulo, Brazil", ["São Paulo Zoo", ["zoo"]])
add_attraction("São Paulo, Brazil", ["Pátio do Colégio", ["historical site"]])
add_attraction("Cairo, Egypt", ["Pyramids of Giza", ["monument", "historical site"]])
add_attraction("Cairo, Egypt", ["Egyptian Museum", ["museum"]])

#print(attractions)

# Finding the Best Places to go
def find_attractions(destination, interests):
    destination_index = get_destination_index(destination)
    attractions_in_city = attractions[destination_index]
    attractions_with_interest = []
    for attraction in attractions_in_city:
        attraction_name = attraction[0]  # Extracting the name of the attraction
        attraction_tags = attraction[1]   # Extracting the tags of the attraction
        for interest in interests:
            if interest in attraction_tags:
                attractions_with_interest.append(attraction_name)
    return attractions_with_interest

#la_arts = find_attractions("Los Angeles, USA", ['art'])
#print(la_arts)


# See The Parts of a city You want to see
def get_attractions_for_traveler(traveler):
    traveler_destination = traveler[1]
    traveler_interests = traveler[2]
    traveler_attractions = find_attractions(traveler_destination, traveler_interests)

    interests_string = "Hi  " + traveler[0] + ", we think you'll like these places around " +  traveler_destination + ":"
  
    for i in range(len(traveler_attractions)):
        if traveler_attractions[-1] == traveler_attractions[i]:
            interests_string += " the " + traveler_attractions[i] + "."
        else:
            interests_string += " the "+ traveler_attractions[i] + ","
    return interests_string


smills_france = get_attractions_for_traveler(['Dereck Smill', 'Paris, France', ['monument']])

print(smills_france)
