from lxml import etree
import csv
import os
from os.path import join

path = 'Real_Masters_all'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    for sub in tree.xpath('//ead/archdesc//controlaccess/*'):
        if sub.tag == 'subject' or sub.tag == 'corpname' or sub.tag == 'geogname' or sub.tag == 'persname' or sub.tag == 'genreform' or sub.tag == 'famname':
            with open('subjects_20150618.csv', 'ab') as csvfile:
                writer = csv.writer(csvfile, dialect='excel')
                if sub.text is not None and 'source' in sub.attrib:
                    writer.writerow([filename, sub.tag, sub.text.encode("utf-8"), sub.attrib['source'], tree.getpath(sub)])
                elif sub.text is not None:
                    writer.writerow([filename, sub.tag, sub.text.encode("utf-8"), '', tree.getpath(sub)])
                else:
                    continue
    print filename
