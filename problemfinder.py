import csv
import lxml
from lxml import etree
import os
from os.path import join

path = 'C:/Users/Public/Documents/Real_Masters_all_2'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    e = tree.xpath('//ead/archdesc/did/physdesc/extent')
    print filename