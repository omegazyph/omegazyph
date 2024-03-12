# Battery Level
user_input = int(input("Enter the battery level\n>> "))

if user_input >=1 and user_input <=5:
    print ("The battery is dead please charge it")

elif user_input >=5 and user_input <= 15:

    print ("You have almost a dead battery, You can charge it")

elif user_input >= 15 and user_input <= 25:
    print ("Your battery is really low, Charge it")

elif user_input >= 25 and user_input <= 45:
    print ("You have medium battery, I recommed you to charge it")

elif user_input >= 45 and user_input <= 60:
    print ("Your battery is good, but don't ues it!")

elif user_input >= 60 and user_input <= 80:
    print ("Your battery is great, use it!")

elif user_input >= 80 and user_input <= 100:
    print ("Your battery is full")

else:
    print ("Can't find the battery")

