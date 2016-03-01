import csv
import os

# Include the path to the starting, freshly exported csv
base_csv = 'C:/Users/djpillen/GitHub/accessions/accessions_20160226.csv'

# Set up the filenames for the additional csvs that will be created
no_null_csv = base_csv.replace('.','-nonull.')
no_blank_rows_csv = base_csv.replace('.','-noblankrows.')
no_blank_ids_csv = base_csv.replace('.','-noblankIDs.')

# we need to rewrite the csv with no null bytes
# first, open the starting csv and read the contents
exported = open(base_csv,'rb')
data = exported.read()
exported.close()

# next, rewrite the csv without null bytes
no_nulls = open(no_null_csv,'wb')
no_nulls.write(data.replace('\x00',''))
no_nulls.close()

# Open the csv
with open(no_null_csv,'rb') as csvfile:
    reader = csv.reader(csvfile)
    # FileMaker exports some fields with the same headers
    # This will make the header row unique
    headers = reader.next()
    headers[29] = "GiftAgreementStatus"
    headers[35] = "ProcessingStatus"
    headers[37] = "RestrictionsType"
    headers[42] = "SeparationsType"
    # Add a header for the to-be-concatenated location info
    headers.append('LocationInfo')
    # Start a new csv by writing the new header row
    with open(no_blank_rows_csv,'ab') as csvout:
        writer = csv.writer(csvout)
        writer.writerow(headers)
    # Remove entirely blank rows
    for row in reader:
        row_indexes = len(row)
        content = False
        # Check for some known columns that are not blank but that are not worth keeping
        if len(row[2]) == 0 and row[21] == 'YYYY':
            for i in range(row_indexes):
                if i != 21 and len(row[i]) != 0:
                    content = True
        # Check the remaining rows for any non-blank columns
        else:
            for i in range(row_indexes):
                if not content:
                    if len(row[i]) != 0:
                        content = True
        # Rewrite the csv with no blank rows
        if content:
            with open(no_blank_rows_csv, 'ab') as csvout:
                writer = csv.writer(csvout)
                writer.writerow(row)


rows = {}
missingid = {}
differences = []

with open(no_blank_rows_csv,'rb') as csvfile:
    reader = csv.reader(csvfile)
    headers = reader.next()
    rows[0] = headers
    count = 1
    # Concatenate the 7 separate location fields
    for row in reader:
        location_indexes = {19:'Old Location/Note Field: ', 44:'Box Range: ',45:'Disk Site: ',46:'Full Path: ',47:'Shelf Range: ',48:'Site: ',49:'Temporary Location Note: '}
        location_info = []
        for i in location_indexes:
            if len(row[i]) > 0:
                location_info.append(location_indexes[i] + row[i])
        if len(location_info) > 0:
            location = '; '.join(location_info)
        else:
            location = ''
        row.append('; '.join(location_info))
        rows[count] = row
        row_indexes = len(row)
        # Some accession ids get exported into multiple rows and will need to be brought back together
        # This checks for rows that are missing an accession id
        if len(row[2]) == 0:
            missingid[count] = []
            for i in range(row_indexes):
                if len(row[i]) != 0:
                    missingid[count].append(i)
        count += 1

# For rows that are missing an accession id, find the accession to which they belong by finding the closest previous row that has an accession id
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
    if the_id != '803':
        for content in contents:
            if len(previous[content]) == 0 and len(current_row[content]) > 0:
                previous[content] = current_row[content]
            elif len(previous[content]) > 0 and (previous[content] != current_row[content]):
                previous[content] = previous[content] + ';;;' + current_row[content]
                if the_id not in differences:
                    differences.append(the_id)

print sorted([int(i) for i in differences])

# Finally, write a csv with no null bytes, no blank rows, and all values for each accession id in one row
with open(no_blank_ids_csv,'ab') as csvfile:
    writer = csv.writer(csvfile)
    for count in rows:
        current_row = rows[count]
        if len(current_row[2]) != 0:
            writer.writerow(current_row)

# Remove the working csvs
# TO DO: Rewrite this so you don't need to create working csvs
os.remove(no_null_csv)
os.remove(no_blank_rows_csv)
