from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    didodd = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]//did/odd")
    if didodd:
        for r in didodd:
            odd = r
            did = r.getparent()
            c = did.getparent()
            c.insert(c.index(did)+1, odd)
        outFile = open((join(path, filename)), 'w')
        outFile.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True,pretty_print=True))
        outFile.close()
        print filename
