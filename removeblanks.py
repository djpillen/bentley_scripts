import csv

file = 'accessions.csv'
outfile = 'accessions2.csv'

with open('accessions.csv','rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
            if len(row[2]) == 0:
                continue
            else:
                with open('accessions2.csv','ab') as csvout:
                        writer = csv.writer(csvout, dialect='excel')
                        writer.writerow(row)