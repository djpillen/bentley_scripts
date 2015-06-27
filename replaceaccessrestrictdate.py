import csv
from lxml import etree
from os.path import join

path = 'S:/Curation/Projects/Mellon/ArchivesSpace/ATeam_Migration/EADs/Real_Masters_all'
with open('accessrestrictdate-flagged-2.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)
    for row in reader:
        filename = row[0]
        xpath = row[1]
        #expression = row[2]
        normalized = row[3]
        print filename + ' ' + normalized
        ead = open(join(path, filename))
        tree = etree.parse(ead)
        date = tree.xpath(xpath)
        #date[0].text = expression
        date[0].attrib['normal'] = normalized
        outfile = open(join(path, filename), 'w')
        outfile.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True))
        outfile.close()
        print 'success!'

print "accessrestrictdate-normal-2 Complete"
