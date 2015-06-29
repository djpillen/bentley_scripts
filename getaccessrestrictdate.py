from lxml import etree
import os
from os.path import join
import re
import csv

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
eads = re.compile(r'\.xml$')
for filename in os.listdir(path):
    if eads.search(filename):
        tree = etree.parse(join(path, filename))
        accessdate = tree.xpath('//archdesc/dsc//accessrestrict//date')
        for a in accessdate:
            if 'normal' in a.attrib:
                normal = a.attrib['normal']
            else:
                normal = ''
            with open('C:/Users/Public/Documents/accessrestrictdate-8.csv', 'ab') as csvfile:
                writer = csv.writer(csvfile, dialect='excel')
                writer.writerow([filename, tree.getpath(a), a.text, normal, etree.tostring(a)])
        print filename
