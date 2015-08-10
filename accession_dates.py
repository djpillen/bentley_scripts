import csv
from datetime import datetime



accessions_file = 'C:/Users/Public/Documents/accessions/accessions_20150810-noblanks.csv'

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
    while accession_dates[null+next_index] == 'null':
        next_index += 1
    previous_date = accession_dates[null-previous_index]
    previous_date_object = datetime.strptime(previous_date, '%m/%d/%Y')
    next_date = accession_dates[null+next_index]
    next_date_object = datetime.strptime(next_date,'%m/%d/%Y')
    previous_year = int(previous_date.split('/')[2])
    next_year = int(next_date.split('/')[2])
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

with open('C:/Users/Public/Documents/accessions/accessions_20150810-noblanks.csv','rb') as csvin, open('C:/Users/Public/Documents/accessions/accessions_20150810-datefix.csv','ab') as csvout:
    reader = csv.reader(csvin)
    writer = csv.writer(csvout, dialect='excel')
    count = -1
    for row in reader:
        accession_description = row[0]
        accession_date = row[1]
        status = row[35]
        if len(accession_date) == 0 and len(accession_description) == 0 and not (status == 'Backlog' or status == 'In Progress'):
            continue
        if len(accession_date) > 0:
            writer.writerow(row)
        elif accession_dates[count] != 'null':
            row[1] = accession_dates[count]
            writer.writerow(row)
        else:
            writer.writerow(row)
        count += 1

with open('C:/Users/Public/Documents/accessions/accessions_20150810-datefix.csv','rb') as csvin, open('C:/Users/Public/Documents/accessions/accessions_20150810-final.csv','ab') as csvout:
    reader = csv.reader(csvin)
    writer = csv.writer(csvout, dialect='excel')
    for row in reader:
        accession_date = row[1]
        accession_description = row[0]
        status = row[35]
        if len(accession_date) == 0 and len(accession_description) == 0 and not (status == 'Backlog' or status == 'In Progress'):
            continue
        else:
            writer.writerow(row)
