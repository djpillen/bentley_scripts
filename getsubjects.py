from lxml import etree
import csv
import os
from os.path import join


tags = ['subject', 'geogname','genreform','title']
subjects = {'subject':{},'geogname':{},'genreform':{},'title':{}}

text_to_authfilenumber = {}

unique_subject_csv = 'C:/Users/djpillen/GitHub/test_run/subjects/ead_unique_subjects_20160208.csv'
text_to_authfilenumber_csv = 'C:/Users/djpillen/GitHub/test_run/subjects/text_to_authfilenumber.csv'

# Get a csv with only unique subjects
path = 'C:/Users/djpillen/GitHub/without-reservations/Real_Masters_all'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    for sub in tree.xpath('//controlaccess/*'):
        if sub.tag in tags and sub.text is not None:
            sub_text = sub.text.encode('utf-8')
            source = sub.attrib['source']
            if source not in subjects[sub.tag]:
                subjects[sub.tag][source] = []
            if sub_text not in subjects[sub.tag][source]:
                subjects[sub.tag][source].append(sub_text)
            if 'authfilenumber' in sub.attrib:
                authfilenumber = sub.attrib['authfilenumber']
                if sub_text not in text_to_authfilenumber:
                    text_to_authfilenumber[sub_text] = authfilenumber
    print 'Processing unique subjects for',filename

print 'Writing unique subject csv'
for subject_type in subjects:
    for source in subjects[subject_type]:
        for subject in subjects[subject_type][source]:
            with open(unique_subject_csv, 'ab') as csvfile:
                row = []
                row.append(subject_type)
                row.append(source)
                row.append(subject)
                terms = subject.split('--')
                for term in terms:
                    row.append(term)
                writer = csv.writer(csvfile, dialect='excel')
                writer.writerow(row)

print "Writing text to authfilenumber csv"
with open(text_to_authfilenumber_csv,'ab') as csvfile:
    writer = csv.writer(csvfile)
    for subject_text in text_to_authfilenumber:
        writer.writerow([subject_text,text_to_authfilenumber[subject_text]])
