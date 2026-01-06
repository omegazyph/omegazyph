import csv

file_path = 'Code Academy Projects/Exam_coding/CSV_reading/employees.csv'

with open(file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row.get('Name', 'N/A')
        phone_number = row.get('Phone Number', 'N/A')
        print(f"{name}: {phone_number}")
