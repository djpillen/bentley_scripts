import lxml
from lxml import etree
import os
from os.path import join
import re

path = 'camelcase'
outFilePath = 'test_eads'
for filename in os.listdir(path):
    print filename
    tree = etree.parse(join(path, filename))
    extent = tree.xpath('//extent')
    alpha_extent = re.compile('^[A-Za-z]')
    for r in extent:
        if r.text is None:
            physdesc = r.getparent()
            physdesc.getparent().remove(physdesc)
        elif r.text is not None and alpha_extent.match(r.text):
            remove_alpha = re.sub('^[A-Za-z]+(.*)?\s','',r.text)
            r.text = remove_alpha
    finish = open(join(outFilePath, filename), 'w')
    finish.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True))
    finish.close()
