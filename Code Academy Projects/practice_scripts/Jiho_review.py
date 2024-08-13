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

#user setup
guest_name = input('What is your name: ')
guest_table_number = int(input("What's the table number: "))

def assign_table(table_number, name, vip_status=False): 
  
  tables[table_number]['name'] = name
  tables[table_number]['vip_status'] = vip_status
  tables[table_number]['order'] = {}

assign_table(guest_table_number,guest_name)
#print(tables[2])















# Table order
guest_drinks = input("What would they like to drink: ")
guest_food = input("What would they like to eat:")

def assign_food_items(table_number, **order_items):
  food = order_items.get('food')
  drinks = order_items.get('drinks')
  tables[table_number]['order']['food_items'] = food
  tables[table_number]['order']['drinks'] = drinks

assign_food_items(guest_table_number, food=[guest_food], drinks=[guest_drinks])
print(tables[guest_table_number])













def calculate_price_per_person(total, tip, split):
    total_tip = total * (tip/100)
    split_price = (total + total_tip) / split
    print('split price',split_price)
#calculate_price_per_person(*tables[1]['order']['total'])