from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

subelements = []

for filename in os.listdir(path):
    print filename
    tree = etree.parse(join(path,filename))
    for subelement in tree.xpath('//p/*'):
        if subelement.tag not in subelements:
            subelements.append(subelement.tag)

print subelements
