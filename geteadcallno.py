from lxml import etree
import os
from os.path import join
import csv

path = 'Real_Masters_all'

for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    callno = tree.xpath('//archdesc/did/unitid')
    coltitle = tree.xpath('//archdesc/did/unittitle')
    with open('eadcallno.csv', 'ab') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow([filename, callno[0].text or 'PROBLEM HERE', coltitle[0].text or 'PROBLEM HERE'])
    print filename
