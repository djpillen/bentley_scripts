import csv

marc_csv = 'C:/Users/Public/Documents/marc_xml-subjects.csv'
ead_csv = 'C:/Users/Public/Documents/ead_subjects_20150731.csv'

marc_list = []
ead_list = []

marc_terms = []
ead_terms = []

def build_list(subject_csv, subject_list, terms_list):
    with open(subject_csv, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            subject = row[0]
            if '--' in subject:
                if subject not in subject_list:
                    subject_list.append(subject)
                for term in subject.strip('.').split('--'):
                    if term not in terms_list:
                        terms_list.append(term)


print "Processing EAD subjects..."
build_list(ead_csv, ead_list, ead_terms)
print "Processing MARC subjects..."
build_list(marc_csv, marc_list, marc_terms)

total_subjects = 0
duplicate_subjects = 0
unique_subjects = 0

print "Checking for duplicate subjects..."
for subject in ead_list:
    total_subjects += 1
    if subject in marc_list:
        duplicate_subjects += 1
    else:
        unique_subjects += 1

total_terms = 0
duplicate_terms = 0
unique_terms = 0

unique_terms_list = []

print "Checking for duplicate terms..."
for term in ead_terms:
    total_terms += 1
    if term in marc_terms:
        duplicate_terms += 1
    else:
        unique_terms +=1
        unique_terms_list.append(term)


print "Total subjects:", total_subjects
print "Duplicate subjects:", duplicate_subjects
print "Unique subjects:", unique_subjects

print "Total terms:", total_terms
print "Duplicate terms:", duplicate_terms
print "Unique terms:", unique_terms


#print unique_terms_list
