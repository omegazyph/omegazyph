name = input("Type your name :> ")
print("Welcome",name, "to this aventure!")

answer = input("You are on a dirt road, it has come to an end and you can go left or right.  Which way would you like to go? :> ").lower()

if answer == "left":
    answer = input("You come tok a river, you can walk around it or swim across? Type walk to walk around or swim to swim across? :> ")
elif answer == "Right":
    print()

else:
    print("Not a vaild option. You lose.")