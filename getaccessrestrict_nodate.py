import lxml
from lxml import etree
import os
from os.path import join
import re
import csv

path = 'Real_Masters_all'
eads = re.compile('\.xml$')
for filename in os.listdir(path):
    if eads.search(filename):
        tree = etree.parse(join(path, filename))
        access = tree.xpath('//archdesc/dsc//accessrestrict')
        for a in access:
            if not a.xpath('.//date'):

                with open('accessrestrict-nodate.csv', 'ab') as csvfile:
                    writer = csv.writer(csvfile, dialect='excel')
                    writer.writerow([filename, tree.getpath(a), etree.tostring(a)])

               