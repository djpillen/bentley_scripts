import lxml
from lxml import etree
import xml.etree.cElementTree as cElementTree
import os
from os.path import join
import csv

path = 'C:/Users/Public/Documents/marc_xml-split'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    callno = tree.xpath('//marc:datafield[@tag="852"]/marc:subfield[@code="h"]', namespaces={'marc': 'http://www.loc.gov/MARC21/slim'})
    coltitle = tree.xpath('//marc:datafield[@tag="245"]/marc:subfield[@code="a"]', namespaces={'marc': 'http://www.loc.gov/MARC21/slim'})
    with open('C:/Users/Public/Documents/marcxmlcallno.csv', 'ab') as csvfile:
            writer = csv.writer(csvfile, dialect='excel')
            try:
                writer.writerow([filename, callno[0].text, coltitle[0].text])
            except:
                writer.writerow([filename, callno[0].text, 'PROBLEM HERE'])
    print filename

