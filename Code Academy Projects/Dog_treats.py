def buy_items(starting_money, starting_num_items, item_price):
    # Initialize a variable to keep track of the number of items bought
    num_bought = 0
    
    # Continue buying items until either there is no more money or no more items left to buy
    while starting_money >= item_price and starting_num_items > 0:
        # Deduct the price of the item from the available money
        starting_money -= item_price
        
        # Decrement the number of available items by 1
        starting_num_items -= 1
        
        # Increment the number of items bought
        num_bought += 1
    
    # Return the total number of items bought
    return num_bought

# Initial values
starting_money = 100
starting_num_items = 10
item_price = 4

# Call the function and store the result in 'total'
total = buy_items(starting_money, starting_num_items, item_price)
print("You were able to buy " + str(total) + " items.")
  
# For testing purposes
total_1 = buy_items(100, 10, 4)
print("Test 1: " + str(total_1))
total_2 = buy_items(10, 10, 4)
print("Test 2: " + str(total_2))
