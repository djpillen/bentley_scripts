from lxml import etree
import os
from os.path import join
import csv


path = 'Real_Masters_all'

for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    odds = tree.xpath('//odd/p')
    for r in odds:
        if r.text is None:
            print filename, tree.getpath(r)
            with open('emptyodds.csv','ab') as csvfile:
                writer = csv.writer(csvfile, dialect='excel')
                writer.writerow([filename, tree.getpath(r)])
