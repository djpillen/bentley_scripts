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
        accesstop = tree.xpath('//archdesc/descgrp/accessrestrict')
        accesscomponent = tree.xpath('//archdesc/dsc//accessrestrict')
        accessdate = tree.xpath('//archdesc/dsc//accessrestrict//date')
        for a in accesstop:
            with open('accessrestrict_toplevel-3.csv', 'ab') as csvfile:
                writer = csv.writer(csvfile, dialect='excel')
                writer.writerow([filename, tree.getpath(a), etree.tostring(a)])
        for a in accesscomponent:
            with open('accessrestrict_component-3.csv', 'ab') as csvfile:
                writer = csv.writer(csvfile, dialect='excel')
                writer.writerow([filename, tree.getpath(a), etree.tostring(a)])
        for a in accessdate:
            if 'normal' in a.attrib:
                normal = a.attrib['normal']
            else:
                normal = ''
            with open('accessrestrictdate-7.csv', 'ab') as csvfile:
                writer = csv.writer(csvfile, dialect='excel')
                writer.writerow([filename, tree.getpath(a), a.text, normal, etree.tostring(a)])
        print filename
               