name = input("Type your name :> ")
print("Welcome",name, "to this aventure!")

answer = input("You are on a dirt road, it has come to an end and you can go left or right.  Which way would you like to go? :> ").lower()
if answer == "left":
    answer = input("You come tok a river, you can walk around it or swim across? Type walk to walk around or swim to swim across? :> ")
    if answer == "swim":
        print("You swam across ane were eaten by an alligator.")
    elif answer == "walk":
        print("You walked for many miles, ran out of water and you lost the game")
    else:
        print("Not a vaild option. You lose.")

elif answer == "Right":
    answer = input("You come to a bridge, it looks wobbly, do you want to cross it, or head back? (cross/back):> ")
    if answer == "back":
        answer = input("You go back and lose:> ")
    if answer == "cross":
        answer = input("You cross the bridge and meet a stanger. Do you talk to them (yesy/no)? :> ").lower()
        if answer == "yes":
            print("You talked to the stanger and they give you gold. You WIN!")
        elif answer == "no":
            print("You ignore the stranger and they were offended and you lose")
        else:
            print("Not a vaild option. You lose.")
else:
    print("Not a vaild option. You lose.")

print("Thank you for trying", name)
