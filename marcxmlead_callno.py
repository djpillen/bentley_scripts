import lxml
from lxml import etree
import xml.etree.cElementTree as cElementTree
import os
from os.path import join
import csv

marcpath = 'C:/Users/Public/Documents/marc_xml-split'
eadpath = 'C:/Users/Public/Documents/Real_Masters_all'
for filename in os.listdir(marcpath):
    tree = etree.parse(join(marcpath, filename))
    callno = tree.xpath('//marc:datafield[@tag="852"]/marc:subfield[@code="h"]', namespaces={'marc': 'http://www.loc.gov/MARC21/slim'})
    coltitle = tree.xpath('//marc:datafield[@tag="245"]/marc:subfield[@code="a"]', namespaces={'marc': 'http://www.loc.gov/MARC21/slim'})
    with open('C:/Users/Public/Documents/marcxmleadcallno.csv', 'ab') as csvfile:
            writer = csv.writer(csvfile, dialect='excel')
            try:
                writer.writerow([filename, 'marc', callno[0].text, coltitle[0].text])
            except:
                writer.writerow([filename, 'marc', callno[0].text, 'PROBLEM HERE'])
    print filename
    
for filename in os.listdir(eadpath):
    tree = etree.parse(join(eadpath, filename))
    callno = tree.xpath('//archdesc/did/unitid')
    coltitle = tree.xpath('//archdesc/did/unittitle')
    with open('C:/Users/Public/Documents/marcxmleadcallno.csv', 'ab') as csvfile:
            writer = csv.writer(csvfile, dialect='excel')
            try:
                writer.writerow([filename, 'ead', callno[0].text, coltitle[0].text])
            except:
                try:
                    writer.writerow([filename, 'ead', callno[0].text, 'PROBLEM HERE'])
                except:
                    writer.writerow([filename, 'ead', 'PROBLEM HERE', coltitle[0].text])
    print filename
