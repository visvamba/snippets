import csv

with open('employee_birthday.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        print(row)

# OR
with open(filename) as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        print(row[key1])
        print(row[key2])