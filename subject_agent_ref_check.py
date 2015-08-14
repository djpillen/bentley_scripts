from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

test_dir = 'C:/Users/djpillen/GitHub/test_dir'

tags = ['subject','geogname','genreform']

for filename in os.listdir(test_dir):
    tree = etree.parse(join(test_dir,filename))
    for sub in tree.xpath('//controlaccess/*'):
        if sub.tag in tags and sub.text is not None:
            if not 'ref' in sub.attrib:
                print filename, sub.text.encode('utf-8')
