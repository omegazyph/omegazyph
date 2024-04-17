pwd = input("What is the master password? :> ")

while True:
    mode = input("Would you like to add a new password or view existing ones (view, add), press Q to Quit:> ").lower()
    if mode == "view":
        pass
    elif mode == "add":
        pass
    else:
        print("Invalid mode")
        continue