import lxml
from lxml import etree
import xml.etree.cElementTree as cElementTree
import os
from os.path import join
import csv
from datetime import datetime

startTime = datetime.now()

marcpath = 'C:/Users/djpillen/GitHub/vandura/marc_xml-split'
eadpath = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

callnos = {}

for filename in os.listdir(marcpath):
    tree = etree.parse(join(marcpath, filename))
    callno = tree.xpath('//marc:datafield[@tag="852"]/marc:subfield[@code="h"]', namespaces={'marc': 'http://www.loc.gov/MARC21/slim'})
    marc_call = callno[0].text.encode('utf-8')
    coltitle = tree.xpath('//marc:datafield[@tag="245"]/marc:subfield[@code="a"]', namespaces={'marc': 'http://www.loc.gov/MARC21/slim'})
    marc_title = coltitle[0].text.encode('utf-8') if coltitle[0].text else ''
    if marc_call not in callnos:
        callnos[marc_call] = []
        callnos[marc_call].append(filename + ' ' + marc_title)
    else:
        callnos[marc_call].append(filename + ' ' + marc_title)
    print filename

for filename in os.listdir(eadpath):
    tree = etree.parse(join(eadpath, filename))
    callno = tree.xpath('//archdesc/did/unitid')
    ead_call = callno[0].text.encode('utf-8')
    coltitle = tree.xpath('//archdesc/did/unittitle')
    ead_title = coltitle[0].text.encode('utf-8') if coltitle[0].text else ''
    if ead_call not in callnos:
        callnos[ead_call] = []
        callnos[ead_call].append(filename + ' ' + ead_title)
    else:
        callnos[ead_call].append(filename + ' ' + ead_title)
    print filename

for k, v in callnos.iteritems():
    if len(v) > 1:
        with open('C:/Users/Public/Documents/duplicate_call_numbers.csv', 'ab') as csvfile:
            writer = csv.writer(csvfile)
            row = [k]
            for item in v:
                row.append(item)
            writer.writerow(row)

print datetime.now() - startTime
