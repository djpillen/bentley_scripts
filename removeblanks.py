import csv
import os

# Only need to change this

base_csv = 'C:/Users/Public/Documents/accessions/accessions_20150921.csv'
no_null_csv = base_csv.replace('.','-nonull.')
no_blank_rows_csv = base_csv.replace('.','-noblankrows.')
no_blank_ids_csv = base_csv.replace('.','-noblankids.')

# we need to rewrite this csv with no null bytes
exported = open(base_csv,'rb')
data = exported.read()
exported.close()

no_nulls = open(no_null_csv,'wb')
no_nulls.write(data.replace('\x00',''))
no_nulls.close()

# rewrite the csv, removing blank rows
with open(no_null_csv,'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        row_indexes = len(row)
        possibilities = [32,34,35,44,45,46,47,48,49,21,26,29]
        content = False
        #if there is no accessionid, the row is entirely blank
        # NOPE. Find a way to check for multiple locations
        if len(row[2]) == 0 and row[21] == 'YYYY':
            for i in range(row_indexes):
                if i != 21 and len(row[i]) != 0:
                    content = True
        else:
            for i in range(row_indexes):
                if not content:
                    if len(row[i]) != 0:
                        content = True
        if content:
            with open(no_blank_rows_csv, 'ab') as csvout:
                writer = csv.writer(csvout, dialect='excel')
                writer.writerow(row)

rows = {}
missingid = {}
differences = []

with open(no_blank_rows_csv,'rb') as csvfile:
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

with open(no_blank_ids_csv,'ab') as csvfile:
    writer = csv.writer(csvfile)
    for count in rows:
        current_row = rows[count]
        if len(current_row[2]) != 0:
            writer.writerow(current_row)


os.remove(no_null_csv)
os.remove(no_blank_rows_csv)
