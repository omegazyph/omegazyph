# zip_longest()


from itertools import zip_longest

list1 = [1,2,3]
list2 = ['a', 'b']

# this will not pick up the 3 value
zipped = zip(list1, list2)
print(list(zipped))

# This will pick up the 3rd value
zipped = zip_longest(list1, list2, fillvalue='N/A')
print(list(zipped))