from lxml import etree
import os
from os.path import join
import re

path = 'C:/Users/Public/Documents/space_tails'
tails = []
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    elems = tree.xpath('//*')
    spaces = re.compile(r'\s')
    dont_replace = re.compile(r"""["'\.,\?\!\-:}\];\s\)\(s]""")
    for r in elems:
        if r.tail and not 'lb' in r.tag:
            #print filename, tree.getpath(r)
            if r.tail[0] not in tails:
                tails.append(r.tail[0])
            else:
                continue
print tails
