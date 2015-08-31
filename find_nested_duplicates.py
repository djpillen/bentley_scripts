from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

okay = ['controlaccess','item','list','descgrp']

for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    elements = tree.xpath('//*')
    for element in elements:
        element_tag = element.tag
        subelements = element.xpath('.//*')
        for subelement in subelements:
            subelement_tag = subelement.tag
            if subelement_tag not in okay:
                if subelement_tag == element_tag:
                    print filename, element_tag, tree.getpath(element)
