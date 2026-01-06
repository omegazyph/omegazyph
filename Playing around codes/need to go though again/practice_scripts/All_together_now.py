def single_prix_fixe_order(appetizer, *entrees, sides, **dessert_scoops):
    """
    Function to handle a prix fixe order with various components.

    Parameters:
    - appetizer (str): The appetizer in the order.
    - *entrees (str): A variable number of entree items.
    - sides (str): The side dish in the order.
    - **dessert_scoops (str): Named dessert options with their respective flavors.
    
    Prints out each part of the order for review.
    """
    # Print the appetizer
    print(f"Appetizer: {appetizer}")
    
    # Print the list of entrees
    print(f"Entrees: {entrees}")
    
    # Print the side dish
    print(f"Sides: {sides}")
    
    # Print each dessert scoop option and its flavor
    print("Dessert Scoops:")
    for dessert, flavor in dessert_scoops.items():
        print(f"  {dessert}: {flavor}")

# Example usage of the function
order1 = single_prix_fixe_order(
    'Baby Beets', 
    'Salmon', 
    'Scallops', 
    sides='Mashed Potatoes', 
    vanilla='Vanilla', 
    cookies='Cookies and Cream'
)
