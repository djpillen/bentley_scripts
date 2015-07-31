import lxml
from lxml import etree
import xml.etree.cElementTree as cElementTree
import os
from os.path import join

counter = 0
file = "C:/Users/Public/Documents/marc_xml/bent_856.xml"
context = etree.iterparse(file)
context = iter(context)
event, root = context.next()

for event, elem in context:
    if event == "end":
        if elem.tag == '{http://www.loc.gov/MARC21/slim}record':
            elem.tail = None
            counter += 1
            outFilePath = 'C:/Users/Public/Documents/marc_xml-has_ead-split'
            outFile = open((join(outFilePath, str(counter) + '.xml')), 'w')
            doc = etree.tostring(elem, encoding="utf-8", xml_declaration=True, pretty_print=True)
            outFile.write(doc)
            outFile.close()
            print counter
# for filename in os.listdir(path):
    # tree = etree.parse(join(path, filename))
    # root = tree.getroot()
    # for elem in root.iter('{http://www.loc.gov/MARC21/slim}record'):
        # outFilePath = 'C:/Users/Public/Documents/marc_xml-split'
        # n = 10000
        # for i in range(n):
            # outFile = open((join(outFilePath, 'file' + str(i) + '.xml')), 'w')
            # doc = etree.tostring(elem, encoding="utf-8", xml_declaration=True, pretty_print=True)
            # outFile.write(doc)
            # outFile.close()


       #print etree.tostring(elem)
    # record = tree.xpath('//marc:record', namespaces={'marc': 'http://www.loc.gov/MARC21/slim'})
    # for r in record:
        # callno = r.xpath('//marc:datafield[@tag="852"]/marc:subfield[@code="h"]', namespaces={'marc': 'http://www.loc.gov/MARC21/slim'})
        # print callno[0].text
        # callno = r.xpath('//marc:datafield[@tag="852"]/marc:subfield[@code="h"]', namespaces={'marc': 'http://www.loc.gov/MARC21/slim'})
        # callno = callno[0].text
        # print callno

        # outFilePath = 'C:/Users/Public/Documents/marc_xml-split'
        # outFile = open((join(outFilePath, callno)), 'w')
        # doc = etree.tostring(r, encoding="utf-8", xml_declaration=True, pretty_print=True)
        # outFile.write(doc)
        # outFile.close()
        #print etree.tostring(r)
    # root = tree.getroot()
    # for elem in root.iter('*'):
        # if elem.tag == '{http://www.loc.gov/MARC21/slim}record':
            # #print etree.tostring(elem)
            # callno = elem.xpath('//{http://www.loc.gov/MARC21/slim}datafield[@tag="852"]/{http://www.loc.gov/MARC21/slim}subfield[@code="h"]')
            # print callno.text
    # record = tree.xpath('//record')
    # for r in record:
        # callno = r.xpath('//datafield[@tag='852']/subfield[@code='h']')
        # outFilePath = 'C:/Users/Public/Documents/marc_xml-split'
        # outFile = open((join(outFilePath, filename)), 'w')
        # doc = etree.tostring(r, encoding="utf-8", xml_declaration=True, doctype='<!DOCTYPE ead PUBLIC "+//ISBN 1-931666-00-8//DTD ead.dtd (Encoded Archival Description (EAD) Version 2002)//EN" "ead.dtd">', pretty_print=True)
        # outFile.write(doc)
        # outFile.close()



          # <datafield tag="852" ind1="8" ind2=" ">
    # <subfield code="a">MiU-H</subfield>
    # <subfield code="b">BENT</subfield>
    # <subfield code="h">2011170 Aa 2</subfield>
