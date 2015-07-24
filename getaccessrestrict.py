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
        accesstop = tree.xpath('//archdesc/descgrp/accessrestrict')
        accesscomponent = tree.xpath('//archdesc/dsc//accessrestrict')
        accessdate = tree.xpath('//archdesc/dsc//accessrestrict//date')
        for a in accesstop:
            with open('C:/Users/Public/Documents/accessrestrict_toplevel-5.csv', 'ab') as csvfile:
                writer = csv.writer(csvfile, dialect='excel')
                writer.writerow([filename, tree.getpath(a), etree.tostring(a)])
        for a in accesscomponent:
            with open('C:/Users/Public/Documents/accessrestrict_component-6.csv', 'ab') as csvfile:
                writer = csv.writer(csvfile, dialect='excel')
                writer.writerow([filename, tree.getpath(a)]) #etree.tostring(a)])
        '''
        for a in accessdate:
            if 'normal' in a.attrib:
                normal = a.attrib['normal']
            else:
                normal = ''
            with open('C:/Users/Public/Documents/accessrestrictdate-8.csv', 'ab') as csvfile:
                writer = csv.writer(csvfile, dialect='excel')
                writer.writerow([filename, tree.getpath(a), a.text, normal, etree.tostring(a)])
        '''
        print filename
