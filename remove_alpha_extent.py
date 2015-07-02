from lxml import etree
import os
from os.path import join
import re


path = 'C:/Users/Public/Documents/test_eads'
for filename in os.listdir(path):
    print filename
    tree = etree.parse(join(path, filename))
    extent = tree.xpath('//extent')
    for r in extent:
        r.text = "1 linear foot"
    finish = open(join(path, filename), 'w')
    finish.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True))
    finish.close()
