# All of our store items
all_items = [["Taffy", 1], ["Chocolate", 2], ["Cup", 5], ["Plate", 10], ["Bowl", 11], ["Silverware", 22]]

# Empty discounted_items list
discounted_items = []

# Your code here
for item in all_items:
  if item[1] % 2 != 0:
    discounted_items.append(item[0])

# For testing purposes: print discounted list
print(discounted_items)