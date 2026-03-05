# Initialize tables dictionary with predefined values and empty tables
tables = {
    1: {
        'name': 'Jiho',
        'vip_status': False,
        'order': {
            'drinks': 'Orange Juice, Apple Juice',
            'food_items': 'Pancakes',
            'total': [534.50, 20.0, 5]
        }
    },
    2: {},
    3: {},
    4: {},
    5: {},
    6: {},
    7: {},
}

# Collect user input for name and table number
guest_name = input("What is your name: ")
guest_table_number = int(input("What's the table number: "))

# Function to assign a table with the guest's name and VIP status
def assign_table(table_number, name, vip_status=False):
    if table_number in tables:
        tables[table_number]['name'] = name
        tables[table_number]['vip_status'] = vip_status
        tables[table_number]['order'] = {}  # Initialize an empty order
    else:
        print("Invalid table number.")  # Handle invalid table number

# Assign the table details based on user input
assign_table(guest_table_number, guest_name)
#print(tables[guest_table_number])  # Uncomment to debug table assignment

# Collect order details from the user
guest_drinks = input("What would they like to drink: ")
guest_food = input("What would they like to eat: ")

# Function to assign food and drinks to the specified table
def assign_food_items(table_number, **order_items):
    if table_number in tables:
        food = order_items.get('food')  # Get food from keyword arguments
        drinks = order_items.get('drinks')  # Get drinks from keyword arguments
        tables[table_number]['order']['food_items'] = food
        tables[table_number]['order']['drinks'] = drinks
    else:
        print("Invalid table number.")  # Handle invalid table number

# Assign food and drink items to the table based on user input
assign_food_items(guest_table_number, 
                  food=[guest_food],
                  drinks=[guest_drinks])
#print(tables[guest_table_number])  # Uncomment to debug order assignment

# Collect and process financial details from the user
try:
    charge = float(input("What is the charge of the meal: "))  # Meal charge
    guest_tip = float(input("What is the agreed amount for a tip: "))  # Tip amount
    people = int(input("How many people in the group: "))  # Number of people

    # Create a list of total, tip, and number of people
    list1 = [charge, guest_tip, people]
    tables[guest_table_number]['order']['total'] = list1  # Store the list in the table's order

    # Function to calculate the price per person including tip
    def calculate_price_per_person(total, tip, split):
        total_tip = total * (tip / 100)  # Calculate the total tip amount
        split_price = (total + total_tip) / split  # Calculate the split price per person
        print('Split price:', split_price, "per person")  # Print the result

    # Extract values from the list and calculate price per person
    total, tip, split = tables[guest_table_number]['order']['total']
    calculate_price_per_person(total, tip, split)

except ValueError:
    # Handle invalid input for charge, tip, or number of people
    print("Invalid input. Please enter numeric values for charge, tip, and people.")
