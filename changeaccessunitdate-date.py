from lxml import etree
import os
from os.path import join



path = 'C:/Users/Public/Documents/Real_Masters_all_2'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    for n in tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]//accessrestrict//unitdate"):
        n.tag = "date"
        outFilePath = 'C:/Users/Public/Documents/accessdate'
        outFile = open((join(outFilePath, filename)), 'w')
        outFile.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True))
        outFile.close()
    print filename
