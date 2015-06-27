from lxml import etree
import os
from os.path import join
import csv

path = 'C:/Users/Public/Documents/Real_Masters_all_2'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    use = tree.xpath('//userestrict')
    for a in use:
        with open('C:/Users/Public/Documents/userestrict.csv', 'ab') as csvfile:
            writer = csv.writer(csvfile, dialect='excel')
            writer.writerow([filename, tree.getpath(a), etree.tostring(a)])
    print filename
