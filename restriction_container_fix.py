from lxml import etree
import os
from os.path import join
import re
import csv

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

moved_count = 0
for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    access_restrict = tree.xpath('//accessrestrict/p')
    moved = re.compile(r'\bto\b')
    for a in access_restrict:
        if moved.search(etree.tostring(a)) and not 'open' in etree.tostring(a):
            print filename, tree.getpath(a)
            moved_count += 1
            with open('C:/Users/Public/Documents/restriction_container_fix-2.csv','ab') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([filename, tree.getpath(a), etree.tostring(a)])

print "Found:"
print moved_count
