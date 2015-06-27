from lxml import etree
import csv
import os
from os.path import join


path = 'Real_Masters_all'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    for cs in tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]"):
        if cs.xpath("./did[1]//unitdate"):
            for date in cs.xpath("./did[1]//unitdate"):
                if date.text == None:
                    titlepath = tree.getpath(cs)
                    csvfile = open('emptydates.csv', 'ab')
                    writer = csv.writer(csvfile, dialect='excel')
                    writer.writerow([filename, titlepath])
                    csvfile.close()
    print filename
