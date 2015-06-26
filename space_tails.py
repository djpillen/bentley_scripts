import lxml
from lxml import etree
import os
from os.path import join
import re

path = 'newead1'
outFilePath = 'newead2'
for filename in os.listdir(path):
    print filename
    tree = etree.parse(join(path, filename))
    elems = tree.xpath('//*')
    dont_replace = re.compile('[\'\.\,\?\!\"\-\:\)\}\]\;\s]')
    for r in elems:
        if r.tail and not 'lb' in r.tag and not dont_replace.match(r.tail):
            r.tail = ' ' + r.tail
    finish = open(join(outFilePath, filename), 'w')
    finish.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True))
    finish.close()
