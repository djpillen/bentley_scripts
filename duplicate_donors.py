import csv
import re

accessions = 'C:/Users/Public/Documents/accessions/beal_export_20150710-noblanks.csv'
donors = {}
donor_numbers = {}
re_text = re.compile(r'\w')

with open(accessions,'rb') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)
    for row in reader:
        first_name = row[20]
        last_name = row[21]
        organization = row[23]
        donor_number = row[26]
        if re_text.search(last_name) and re_text.search(organization):
            if donor_number not in donors:
                donors[donor_number] = {}
                donors[donor_number]['Person'] = first_name + ' ' + last_name
                donors[donor_number]['Organization'] = organization
        if donor_number not in donor_numbers:
            donor_numbers[donor_number] = []
        elif donor_number in donor_numbers:
            if re_text.search(last_name) and last_name not in donor_numbers[donor_number]:
                donor_numbers[donor_number].append(last_name)
            if re_text.search(organization) and organization not in donor_numbers[donor_number]:
                donor_numbers[donor_number].append(organization)


with open('C:/Users/Public/Documents/accessions/duplicate_donors.csv', 'ab') as csvout:
    writer = csv.writer(csvout, dialect='excel')
    for donor_number in donors:
        writer.writerow([donor_number, donors[donor_number]['Person'], donors[donor_number]['Organization']])

with open('C:/Users/Public/Documents/accessions/duplicate_donor_numbers.csv','ab') as csvout:
    writer = csv.writer(csvout, dialect='excel')
    for donor_number in donor_numbers:
        if len(donor_numbers[donor_number]) > 1 and donor_number not in donors:
            writer.writerow([donor_number, donor_numbers[donor_number]])
