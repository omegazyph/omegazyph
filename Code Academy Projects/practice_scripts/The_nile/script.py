from nile import get_distance, format_price, SHIPPING_PRICES
from test import test_function

# Define calculate_shipping_cost() here:
def calculate_shipping_cost(from_coords, to_coords, shipping_type='Overnight'):
    # Unpack coordinates
    from_lat, from_long = from_coords
    to_lat, to_long = to_coords
    
    # Calculate the distance between the coordinates
    distance = get_distance(*from_coords, *to_coords)
    
    # Get the cost per unit distance based on the shipping type
    cost = SHIPPING_PRICES[shipping_type]
    
    # Calculate the total price based on distance and cost per unit distance
    price = distance * cost
    
    # Format the price for output
    return format_price(price)

# Test the function by calling
# test_function(calculate_shipping_cost)

# Define calculate_driver_cost() here
def calculate_driver_cost(distance, *drivers):
    cheapest_driver = None
    cheapest_driver_price = None

    # Iterate through the list of drivers to find the cheapest one
    for driver in drivers:
        # Calculate the time needed for the driver to cover the distance
        driver_time = distance / driver.speed
        
        # Calculate the total cost for this driver
        price_for_driver = driver.salary * driver_time
        
        # Check if this is the first driver or if this driver is cheaper
        if cheapest_driver is None or price_for_driver < cheapest_driver_price:
            cheapest_driver = driver
            cheapest_driver_price = price_for_driver
    
    # Return the cheapest driver's cost and the driver object
    return cheapest_driver_price, cheapest_driver

# Test the function by calling
# test_function(calculate_driver_cost)

# Define calculate_money_made() here
def calculate_money_made(**trips):
    total_money_made = 0 

    # Iterate through the trips dictionary
    for trip_id, trip in trips.items():
        # Calculate the revenue for each trip (trip cost minus driver cost)
        trip_revenue = trip.cost - trip.driver.cost
        
        # Add the revenue to the total
        total_money_made += trip_revenue
    
    # Return the total money made from all trips
    return total_money_made

# Test the function by calling
# test_function(calculate_money_made)
