import lxml
from lxml import etree
from lxml.etree import tostring
import csv
import os
from os.path import join
import re


path = 'C:/Users/Public/Documents/dates'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    for cs in tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]"):
        if cs.xpath("./did[1]//unitdate"):
            for date in cs.xpath("./did[1]//unitdate"):
                if date.text is None:
                    date.getparent().remove(date)
                    
    outFilePath = 'C:/Users/Public/Documents/datesremoved'
    outFile = open((join(outFilePath, filename)), 'w')
    outFile.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True))
    outFile.close()

                    # titlepath = tree.getpath(cs)
                    # csvfile = open('C:/Users/Public/Documents/mimediafdates.csv', 'ab')
                    # writer = csv.writer(csvfile, dialect='excel')
                    # writer.writerow([filename, titlepath])
                    # csvfile.close()