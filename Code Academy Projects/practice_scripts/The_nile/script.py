from nile import get_distance, format_price, SHIPPING_PRICES
from test import test_function

# Define calculate_shipping_cost() here:
def calulate_shipping_cost(from_coords, 
                           to_coords, 
                           shipping_type):
    from_lat,from_long = from_coords
    to_lat, to_long = to_coords
    distance = get_distance(*from_coords, *to_coords)
    SHIPPING_PRICES[shipping_type]


# Test the function by calling 
# test_function(calculate_shipping_cost)

# Define calculate_driver_cost() here


# Test the function by calling 
# test_function(calculate_driver_cost)

# Define calculate_money_made() here


# Test the function by calling 
# test_function(calculate_money_made)
