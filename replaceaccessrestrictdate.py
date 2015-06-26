import csv
import lxml
from lxml import etree
import os
from os.path import join

path = 'S:/Curation/Projects/Mellon/ArchivesSpace/ATeam_Migration/EADs/Real_Masters_all'
with open('accessrestrictdate-flagged-2.csv', 'rb') as file:
    reader = csv.reader(file)
    next(reader, None)
    for row in reader:
        filename = row[0]
        xpath = row[1]
        #expression = row[2]
        normalized = row[3]
        print filename + ' ' + normalized
        try:
            file = open(join(path, filename))
            tree = etree.parse(file)
            date = tree.xpath(xpath)
            #date[0].text = expression
            date[0].attrib['normal'] = normalized
            outfile = open(join(path, filename), 'w')
            outfile.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True))
            outfile.close()
            print 'success!'
        except:
            outfile = open('accessrestrictdateerrors.txt','a')
            outfile.write(filename + ' ' + normalized)
            outfile.close()
            print 'oops!'
            
        
print "accessrestrictdate-normal-2 Complete"