from lxml import etree
import os
from os.path import join
import csv

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    callno = tree.xpath('//archdesc/did/unitid')
    coltitle = tree.xpath('//archdesc/did/unittitle')
    with open('C:/Users/Public/Documents/eadcallno.csv', 'ab') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow([filename, callno[0].text.encode('utf-8') or '', coltitle[0].text.encode('utf-8') or ''])
    print filename
