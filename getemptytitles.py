from lxml import etree
import os
from os.path import join

print "Searching for empty titles..."
empties = []
path = 'Real_Masters_all'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    for cs in tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]"):
        t = cs.xpath("./did[1]//unittitle/text()")
        subt = cs.xpath("./did[1]//unittitle/*/text()")
        d = cs.xpath("./did[1]//unitdate/text()")
        titlepath = tree.getpath(cs)
        if len(t) == 0 and len(subt) == 0 and len(d) == 0:
            print filename, titlepath
            empties.append(filename)

if len(empties) > 0:
    print "You have empty titles"
else:
    print "No empty titles found!"
'''
            csvfile = open('emptytitles-updates.csv', 'ab')
            writer = csv.writer(csvfile, dialect='excel')
            writer.writerow([filename, titlepath])
            csvfile.close()
    print filename
'''
