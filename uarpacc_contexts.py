from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    coll_title = tree.xpath('//archdesc/did/unittitle')[0]
    coll_title = etree.tostring(coll_title)
    extptrs = tree.xpath('//extptr')
    for extptr in extptrs:
        if extptr.attrib['href'] == 'uarpacc':
            if 'University of Michigan' not in coll_title:
                print filename
