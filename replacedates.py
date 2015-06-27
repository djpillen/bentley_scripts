import csv
from lxml import etree
from os.path import join

path = 'normalized'

with open('normal_dates-20150626.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)
    for row in reader:
        filename = row[0]
        print filename
        xpath = row[1]
        expression = row[3]
        #begin = row[4]
        #end = row[5]
        normalized = row[4]
        ead = open(join(path, filename))
        tree = etree.parse(ead)
        date = tree.xpath(xpath)
        date[0].text = expression
        date[0].attrib['normal'] = normalized
        #date[0].attrib['certainty'] = "approximate"
        outfile = open(join(path, filename), 'w')
        outfile.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True))
        outfile.close()

print "Normalization Complete"
