from lxml import etree
import os
from os.path import join
import csv

posted_subjects_csv = 'C:/Users/Public/Documents/subjects_agents/posted_subjects.csv'
path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
test_dir_in = 'C:/Users/Public/Documents/aspace_migration/test_eads'
test_dir_out = 'C:/Users/Public/Documents/aspace_migration/test_eads'

posted_subjects = {'geogname':{},'genreform':{},'subject':{}}

tags = ['geogname','genreform','subject']

with open(posted_subjects_csv,'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        tag = row[0]
        source = row[1]
        subject = row[2]
        uri = row[-1]
        if source not in posted_subjects[tag]:
            posted_subjects[tag][source] = {}
        posted_subjects[tag][source][subject] = uri

for filename in os.listdir(test_dir_in):
    print "Adding subject uris to {0}".format(filename)
    tree = etree.parse(join(test_dir_in,filename))
    for sub in tree.xpath('//controlaccess/*'):
        if sub.tag in tags and sub.text is not None:
            tag = sub.tag
            source = sub.attrib['source']
            subject = sub.text.encode('utf-8')
            if subject in posted_subjects[tag][source]:
                sub.attrib['ref'] = posted_subjects[tag][source][subject]

    with open(join(test_dir_out,filename),'w') as ead_out:
        ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))
