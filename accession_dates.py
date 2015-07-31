import csv



accessions_file = 'C:/Users/Public/Documents/accessions/accessions-20150729-final.csv'

accession_dates = []
possible_dates = []

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
    next_date = accession_dates[null+next_index]
    previous_year = int(previous_date.split('/')[2])
    next_year = int(next_date.split('/')[2])
    if next_year >= previous_year:
        difference = next_year - previous_year
    else:
        difference = previous_year - next_year
    if difference == 0:
        possible_dates.append(next_year)
    print null, '-', null-previous_index, '(-' + str(previous_index) + '):', previous_date, '|', null+next_index, '(+' + str(next_index) + '):', next_date, '|', 'Difference:', difference

print 'Total nulls:', len(nulls)
print 'Total possible dates:', len(possible_dates)
print 'Remaining nulls:', len(nulls) - len(possible_dates)
