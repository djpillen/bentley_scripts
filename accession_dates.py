import csv
from datetime import datetime
import os



# Replace this with the path to the preprocesed csv created by accessions_preprocessing.py
accessions_file = 'C:/Users/djpillen/GitHub/accessions/accessions_20160226-noblankIDs.csv'
date_fix = accessions_file.replace('-noblankIDs','-datefix')
final_csv = accessions_file.replace('-noblankIDs','-final')

accession_dates = []
possible_dates = 0

with open(accessions_file,'rb') as csvfile:
    reader = csv.reader(csvfile)
    next(reader,None)
    for row in reader:
        accession_date = row[1]
        if len(accession_date) > 0:
            accession_dates.append(accession_date)
        else:
            accession_dates.append('null')

nulls = [date for date in range(len(accession_dates)) if accession_dates[date] == 'null']

for null in nulls:
    previous_index = 1
    next_index = 1
    while accession_dates[null-previous_index] == 'null':
        previous_index += 1
    try:
        while accession_dates[null+next_index] == 'null':
            next_index += 1
    except:
        next_index = 0
    if previous_index > 3:
        previous_index = 3
    if next_index > 3:
        next_index = 3
    if accession_dates[null-previous_index] != 'null':
        previous_date = accession_dates[null-previous_index]
        previous_date_object = datetime.strptime(previous_date, '%m/%d/%Y')
    else:
        previous_date = False
    if accession_dates[null+next_index] != 'null':
        next_date = accession_dates[null+next_index]
        next_date_object = datetime.strptime(next_date,'%m/%d/%Y')
    else:
        next_date = False
    if next_date and previous_date:
        if next_date_object >= previous_date_object:
            difference = next_date_object - previous_date_object
            middle_date = next_date_object - (difference/2)
        else:
            difference = previous_date_object - next_date_object
            middle_date = previous_date_object - (difference/2)
        if difference.days <= 365:
            possible_dates += 1
            accession_dates[null] = middle_date.strftime('%m/%d/%Y')
        print null, '-', null-previous_index, '(-' + str(previous_index) + '):', previous_date, '|', null+next_index, '(+' + str(next_index) + '):', next_date, '|', 'Difference:', difference.days, '|', 'Middle:',middle_date.strftime('%m/%d/%Y')

print 'Total nulls:', len(nulls)
print 'Total possible dates:', possible_dates
print 'Remaining nulls:', len(nulls) - possible_dates

with open(accessions_file,'rb') as csvin, open(date_fix,'ab') as csvout:
    reader = csv.reader(csvin)
    writer = csv.writer(csvout)
    count = -1
    for row in reader:
        accession_date = row[1]
        if len(accession_date) > 0:
            writer.writerow(row)
        elif accession_dates[count] != 'null':
            row[1] = accession_dates[count]
            #To do - add general note indicating that this date is a guess
            writer.writerow(row)
        else:
            writer.writerow(row)
        count += 1

with open(date_fix,'rb') as csvin, open(final_csv,'ab') as csvout:
    reader = csv.reader(csvin)
    writer = csv.writer(csvout)
    removed = 0
    for row in reader:
        accession_date = row[1]
        accession_description = row[0]
        status = row[35]
        donor_number_id = row[9]
        donor_number = row[26]
        if len(accession_date) == 0 and ((len(accession_description) == 0 and len(status) == 0) or donor_number == '1771'):
            removed += 1
            continue
        else:
            writer.writerow(row)
    print 'Removed:', removed

os.remove(accessions_file)
os.remove(date_fix)
