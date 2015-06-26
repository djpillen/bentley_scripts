from lxml import etree
import os
from os.path import join
import re

path = 'C:/Users/Public/Documents/daos'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    for dao in tree.xpath(".//dao"):
        href = dao.get('href')
        dspace = re.compile('^http://hdl.handle.net/')
        if dspace.match(href):
            outFilePath = 'C:/Users/Public/Documents/dspace'
            outFile = open((join(outFilePath, filename)), 'w')
            outFile.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True))
            outFile.close()
        else:
            outFilePath = 'C:/Users/Public/Documents/notdspace'
            outFile = open((join(outFilePath, filename)), 'w')
            outFile.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True))
            outFile.close()
            