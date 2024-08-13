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

# Welcome the Guest
print("Hello Welcome to Jiho Restaurant")

# ask for there name
Guest_name = input("Can i get your name: ")


# show them to there table
print("Thank you",Guest_name,"Right this way I'll take you to your table")
time.sleep(5)

# showing the table
print("Here you go",Guest_name,"a waitress will be here shortly")

# See if the guest is a vip
Guest_vip = input(Guest_name,"are you a vip mamber: yes or no")



# tablenumber
table_number = input("What is the number number 1-7: ")




# functions
def assign_table(table_number, name, vip_status=False): 
  
  tables[table_number]['name'] = name
  tables[table_number]['vip_status'] = vip_status
  tables[table_number]['order'] = {}



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