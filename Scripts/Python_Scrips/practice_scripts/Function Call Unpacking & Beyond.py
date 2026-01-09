def calculate_price_per_person(total, tip, split):
    """
    Calculate the price per person including tip.

    Parameters:
    total (float): The total amount of the bill before tip.
    tip (float): The tip percentage to be added to the total.
    split (int): The number of people to split the total bill.

    Returns:
    None: This function prints the price per person.
    """
    # Calculate the total amount of tip
    total_tip = total * (tip / 100)
    
    # Calculate the total amount including tip
    total_with_tip = total + total_tip
    
    # Calculate the price per person
    split_price = total_with_tip / split
    
    # Print the price per person
    print(f"Price per person: ${split_price:.2f}")

# Data for table 7
table_7_total = [534.50, 20.0, 5]

# Call the function with the values from table_7_total
calculate_price_per_person(*table_7_total)
