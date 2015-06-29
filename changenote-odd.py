from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    notes = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]//note")
    if notes:
        for n in notes:
            n.tag = "odd"
        outFile = open((join(path, filename)), 'w')
        outFile.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True))
        outFile.close()
    print filename
