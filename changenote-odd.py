from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    notes = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]//note")
    if notes:
        for note in notes:
            note.tag = "odd"
        outFile = open((join(path, filename)), 'w')
        with open(join(path,filename),'w') as f:
        	f.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True, pretty_print=True))
        print filename
