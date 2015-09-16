from lxml import etree
import os
from os.path import join
import re

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
digits = re.compile(r'\d')

for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    physdescs = tree.xpath('//physdesc')
    for physdesc in physdescs:
            extents = physdesc.xpath('./extent')
            if extents:
                    extent_text = extents[0].text
                    if not digits.match(extent_text):
                            print filename, extent_text
