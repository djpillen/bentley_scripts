from lxml import etree
import os
from os.path import join
import re
import csv


path = 'C:/Users/Public/Documents/daos'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    for dao in tree.xpath('.//dao'):
        #if 'href' in dao.attrib:
        href = dao.get('href')
        handle = re.compile('^http://hdl.handle.net/2027')
        if not handle.match(href):
            with open('C:/Users/Public/Documents/hrefs.csv', 'ab') as csvfile:
                writer = csv.writer(csvfile, dialect='excel')
                writer.writerow([filename, href])
    print filename
