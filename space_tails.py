from lxml import etree
import os
from os.path import join
import re

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
outFilePath = 'C:/Users/Public/Documents/space_tails'
for filename in os.listdir(path):
    print filename
    tree = etree.parse(join(path, filename))
    elems = tree.xpath('//*')
    dont_replace = re.compile(r"""["'\.,\?\!\-:}\];\s\)\(s]""")
    for r in elems:
        if r.tail and not 'lb' in r.tag and not dont_replace.match(r.tail):
            r.tail = ' ' + r.tail
    finish = open(join(outFilePath, filename), 'w')
    finish.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True))
    finish.close()
