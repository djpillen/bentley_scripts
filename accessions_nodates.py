import csv

accessions_csv = 'C:/Users/Public/Documents/accessions/accessions_20150916-final.csv'

with open(accessions_csv,'rb') as csv_file:
    reader = csv.reader(csv_file)
    next(reader,None)
    for row in reader:
        accession_date = row[1]
        if len(accession_date) == 0:
            with open('C:/Users/Public/Documents/accessions/accessions_20150916-nodates.csv','ab') as csv_out:
                writer = csv.writer(csv_out, dialect='excel')
                writer.writerow(row)
