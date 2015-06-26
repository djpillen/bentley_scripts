import lxml
from lxml import etree
import xml.etree.cElementTree as cElementTree
import os
from os.path import join
import csv

path = 'marc_xml-split'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    extent = tree.xpath('//marc:datafield[@tag="300"]/marc:subfield[@code="a"]', namespaces={'marc': 'http://www.loc.gov/MARC21/slim'}) 
    try:
        e = extent[0].text
    except:
        e = "PROBLEM WITH EXTENT"
    callno = tree.xpath('//marc:datafield[@tag="852"]/marc:subfield[@code="h"]', namespaces={'marc': 'http://www.loc.gov/MARC21/slim'})
    try:
        cn = callno[0].text
    except:
        cn = "PROBLEM WITH CALLNO"
    coltitle = tree.xpath('//marc:datafield[@tag="245"]/marc:subfield[@code="a"]', namespaces={'marc': 'http://www.loc.gov/MARC21/slim'})
    try:
        ct = coltitle[0].text
    except:
        ct = "PROBLEM WITH COLTITLE"
    with open('C:/Users/Public/Documents/marcxmlextents.csv', 'ab') as csvfile:
            writer = csv.writer(csvfile, dialect='excel')
            try:
                writer.writerow([filename, cn, ct, e])
            except:
                writer.writerow([filename, cn, 'ENCODING ERROR', e])
    print filename

