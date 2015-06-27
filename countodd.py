from lxml import etree
import os
from os.path import join

oddpath = 'S:/Curation/Projects/Mellon/ArchivesSpace/ATeam_Migration/EADs/Real_Masters_all'
notepath = 'S:/Curation/Projects/Mellon/ArchivesSpace/ATeam_Migration/EADs/FindingAids-EAD-Master_20150514'
notecounter = []
oddcounter = []
for filename in os.listdir(oddpath):
    tree = etree.parse(join(oddpath, filename))
    odd = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]//odd")
    for r in odd:
        oddcounter.append('1')

print 'Updated odds'
print len(str(oddcounter))

for filename in os.listdir(notepath):
    tree = etree.parse(join(notepath, filename))
    note = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]//note")
    for r in note:
        notecounter.append('1')


print 'Original notes'
print len(str(notecounter))
