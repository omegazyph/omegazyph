#################################################
# Autor wayne Stock
# date 2026-08-21
# Basic Email Validation
################################################

email = input("Enter your Email: ")

if "@" in email and "." in email:
    print (" Vaild Email")
else:
    print("Invaild Email")