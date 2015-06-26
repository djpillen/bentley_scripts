import lxml
from lxml import etree
import os
from os.path import join
import re
import csv

path = 'Real_Masters_all'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    d = tree.xpath('//unitdate')
    for i in d:
        if 'normal' in i.attrib:
            normal = i.attrib['normal']
            with open('normalattributes-8.csv', 'ab') as csvfile:
                writer = csv.writer(csvfile, dialect='excel')
                writer.writerow([filename, tree.getpath(i), normal])
        else:
            continue
    print filename