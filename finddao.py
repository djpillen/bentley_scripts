from lxml import etree
import os
from os.path import join

path = 'C:/Users/Public/Documents/Real_Masters_all'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    if tree.xpath("//dao"):
        outFilePath = 'C:/Users/Public/Documents/daos'
        outFile = open((join(outFilePath, filename)), 'w')
        outFile.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True))
        outFile.close()
        continue