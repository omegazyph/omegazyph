# Fill in your code below
import csv
with open("Code Academy Projects/Exam_coding/CSV_reading/employees.csv", "r") as handler:
 reader = csv.reader(handler, delimiter=',')
 for row in reader:
   print(row)

