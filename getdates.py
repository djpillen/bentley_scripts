import csv
from lxml import etree
import os
from os.path import join
import re


path = 'path/to/EADs'

for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    dates = tree.xpath('//unitdate')
    undated = re.compile('^[Uu](ndated)$')
    for date in dates:
        if date.text and not undated.match(date.text) and not 'normal' in date.attrib:
            with open('path/to/output.csv', 'ab') as csvfile:
                writer = csv.writer(csvfile, dialect='excel')
                writer.writerow([filename, tree.getpath(date), date.text.encode('utf-8')])
    print filename
