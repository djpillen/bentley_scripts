from lxml import etree
import os
from os.path import join

path = 'new3'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    for n in tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]//note"):
        n.tag = "odd"
    outFilePath = 'new4'
    outFile = open((join(outFilePath, filename)), 'w')
    outFile.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True))
    outFile.close()
    print filename