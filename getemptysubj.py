from lxml import etree
import os
from os.path import join
import csv


path = 'C:/Users/Public/Documents/spec_coll_ead_pp'

for filename in os.listdir(path):
    print filename
    tree = etree.parse(join(path,filename))
    for sub in tree.xpath('//ead/archdesc//controlaccess/*'):
        if sub.tag == 'subject' or sub.tag == 'corpname' or sub.tag == 'geogname' or sub.tag == 'persname' or sub.tag == 'genreform' or sub.tag == 'famname':
            if sub.text is None:
                with open('C:/Users/Public/Documents/spec_coll_missing_subjects-1.csv','ab') as csvfile:
                    writer = csv.writer(csvfile,dialect='excel')
                    writer.writerow([filename,sub.tag,tree.getpath(sub)])
