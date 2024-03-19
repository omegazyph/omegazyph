# Fill in your code below
import csv
with open("employees.csv", "r") as handler:
 reader = csv.reader(handler, delimiter=',')
 for row in reader:
   print(row)

