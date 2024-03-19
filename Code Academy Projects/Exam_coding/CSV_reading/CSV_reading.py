# Fill in your code below
import csv

input_file = csv.DictReader(open("Code Academy Projects/Exam_coding/CSV_reading/employees.csv"))
reader = csv.reader(input_file, delimiter=',')
for row in input_file:
   print(row)