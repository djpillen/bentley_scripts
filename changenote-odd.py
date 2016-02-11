from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/without-reservations/Real_Masters_all'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    notes = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]//note")
    if notes:
        for note in notes:
            note.tag = "odd"
        outFile = open((join(path, filename)), 'w')
        outFile.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True, pretty_print=True))
        outFile.close()
        print filename
