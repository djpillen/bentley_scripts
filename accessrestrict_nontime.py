import csv

file = 'accessrestrict-nodate.csv'

non_time = {}
with open(file, 'rb') as no_date_csv:
    reader = csv.reader(no_date_csv)
    for row in reader:
        filename = row[0]
        if filename not in non_time:
            non_time[filename] = 1
        else:
            non_time[filename] += 1
            
for filename in non_time:
    print filename
    print non_time[filename]