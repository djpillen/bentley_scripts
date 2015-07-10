from lxml import etree
import os
from os.path import join
import csv


path = 'C:/Users/Public/Documents/spec_coll_ead_pp'

for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    odds = tree.xpath('//odd/p')
    for r in odds:
        if r.text is None:
            print filename, tree.getpath(r)
            with open('C:/Users/Public/Documents/spec_coll_missing_odds.csv','ab') as csvfile:
                writer = csv.writer(csvfile, dialect='excel')
                writer.writerow([filename, tree.getpath(r)])
