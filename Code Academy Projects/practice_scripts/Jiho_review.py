#imports
import time



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
guest_name = input('What is your name: ')

guest_table_number = int(input("What's the table number: "))

# functions
def assign_table(table_number, name, vip_status=False): 
  
  tables[table_number]['name'] = name
  tables[table_number]['vip_status'] = vip_status
  tables[table_number]['order'] = {}

assign_table(guest_table_number,guest_name)
#print(tables[2])






def assign_food_items(table_number, **order_items):
  food = order_items.get('food')
  drinks = order_items.get('drinks')
  tables[table_number]['order']['food_items'] = food
  tables[table_number]['order']['drinks'] = drinks

def calculate_price_per_person(total, tip, split):
    total_tip = total * (tip/100)
    split_price = (total + total_tip) / split
    print('split price',split_price)
#calculate_price_per_person(*tables[1]['order']['total'])