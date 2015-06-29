from lxml import etree
import os
from os.path import join
import csv


path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

for filename in os.listdir(path):
    print filename
    tree = etree.parse(join(path,filename))
    for sub in tree.xpath('//ead/archdesc//controlaccess/*'):
        if sub.tag == 'subject' or sub.tag == 'corpname' or sub.tag == 'geogname' or sub.tag == 'persname' or sub.tag == 'genreform' or sub.tag == 'famname':
            if sub.text is None:
                with open('C:/Users/Public/Documents/emptysubj-4.csv','ab') as csvfile:
                    writer = csv.writer(csvfile,dialect='excel')
                    writer.writerow([filename,sub.tag,tree.getpath(sub)])
