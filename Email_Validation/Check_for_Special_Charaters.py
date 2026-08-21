#################################################
# Autor wayne Stock
# date 2026-08-21
# Check for Special characters
################################################

import re

email = input("Enter your Email: ")

pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

if re.match(pattern,email):
    print (" Vaild Email")
else:
    print("Invaild Email")