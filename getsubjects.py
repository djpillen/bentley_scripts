from lxml import etree
import csv
import os
from os.path import join


tags = ['subject', 'geogname']

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    for sub in tree.xpath('//controlaccess/*'):
        if sub.tag in tags and sub.text is not None:
            with open('C:/Users/Public/Documents/ead_subjects_20150731.csv', 'ab') as csvfile:
                writer = csv.writer(csvfile, dialect='excel')
                writer.writerow([sub.text.encode("utf-8")])
    print filename
