import csv
import os

# we need to rewrite this csv with no null bytes
exported = open('C:/Users/Public/Documents/accessions/accessions_20150810.csv','rb')
data = exported.read()
exported.close()

no_nulls = open('C:/Users/Public/Documents/accessions/accessions_20150810-nonull.csv','wb')
no_nulls.write(data.replace('\x00',''))
no_nulls.close()

# rewrite the csv, removing blank rows
with open('C:/Users/Public/Documents/accessions/accessions_20150810-nonull.csv','rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        #if there is no accessionid, the row is entirely blank
        if len(row[2]) == 0:
            continue
        else:
            with open('C:/Users/Public/Documents/accessions/accessions_20150810-noblanks.csv', 'ab') as csvout:
                writer = csv.writer(csvout, dialect='excel')
                writer.writerow(row)

os.remove('C:/Users/Public/Documents/accessions/accessions_20150810-nonull.csv')
