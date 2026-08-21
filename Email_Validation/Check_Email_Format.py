#################################################
# Autor wayne Stock
# date 2026-08-21
# Check Email Format
################################################

email = input("Enter your Email: ")

if email.count("@") == 1 and email.endswith((".com",".org", ".net")):
    print (" Vaild Email")
else:
    print("Invaild Email")