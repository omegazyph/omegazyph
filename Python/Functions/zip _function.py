# zip_longest()


from itertools import zip_longest

list1 = [1,2,3]
list2 = ['a', 'b']
list3 = ['True', 'False', 'True']

print("zipped lists")
# this will not pick up the 3 value
zipped = zip(list1, list2, list3)
print(list(zipped))
print("\n")

print("added empty value")
# This will pick up the 3rd value
zipped = zip_longest(list1, list2, list3, fillvalue='N/A')
print(list(zipped))


print("\n")
print("unzipped lists")
# to unzip the lists
zipped = [(1, 'a', 'True'), (2, 'b', 'False'), (3, 'N/A', 'True')]
unzipped = zip(*zipped)

print(list1)
print(list2)
print(list3)