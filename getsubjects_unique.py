from lxml import etree
import csv
import os
from os.path import join

path = 'Real_Masters_all'
subjects = []
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    for sub in tree.xpath('//ead/archdesc//controlaccess/*'):
        if sub.tag == 'subject' or sub.tag == 'corpname' or sub.tag == 'geogname' or sub.tag == 'persname' or sub.tag == 'genreform' or sub.tag == 'famname':
            with open('subjects_20150618.csv', 'ab') as csvfile:
                writer = csv.writer(csvfile, dialect='excel')
                if sub.text is not None and 'source' in sub.attrib:
                    sub_and_source = sub.text.encode('utf-8') +'///'+sub.attrib['source']
                    if sub_and_source not in subjects:
                        subjects.append(sub_and_source)
                elif sub.text is not None and not 'source' in sub.attrib:
                    sub_and_source = sub.text.encode('utf-8') +'///unknown'
                    if sub_and_source not in subjects:
                        subjects.append(sub_and_source)
                else:
                    continue

    print filename

print len(subjects)

for i in subjects:
    with open('subjects_unique_20150618.csv','ab') as csvfile:
        writer = csv.writer(csvfile,dialect='excel')
        writer.writerow([i])
