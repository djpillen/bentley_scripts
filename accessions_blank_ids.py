import csv
import os

accession_csv = 'C:/Users/Public/Documents/accessions/accessions_20150921-noblanks.csv'

rows = {}
missingid = {}
differences = []

with open(accession_csv,'rb') as csvfile:
    count = 0
    reader = csv.reader(csvfile)
    for row in reader:
        rows[count] = row
        row_indexes = len(row)
        if len(row[2]) == 0:
            missingid[count] = []
            for i in range(row_indexes):
                if len(row[i]) != 0:
                    missingid[count].append(i)
        count += 1

for count in missingid:
    current_row = rows[count]
    found_id = False
    subtract = 1
    while found_id is False:
        previous_check = rows[count-subtract]
        if len(previous_check[2]) != 0:
            previous = previous_check
            the_id = previous[2]
            found_id = True
        else:
            subtract += 1
    contents = missingid[count]
    different = False
    for content in contents:
        if previous[content] != current_row[content]:
            different = True
    if different:
        for content in contents:
            previous[content] = previous[content] + ';;;' + current_row[content]
        if the_id not in differences:
            differences.append(the_id)

print sorted([int(i) for i in differences])

with open('C:/Users/Public/Documents/accessions/accessions_20150921-final.csv','ab') as csvfile:
    writer = csv.writer(csvfile)
    for count in rows:
        current_row = rows[count]
        if len(current_row[2]) != 0:
            writer.writerow(current_row)

os.remove(accession_csv)
