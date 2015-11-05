from lxml import etree
import os
from os.path import join
import re

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    lists = tree.xpath('//list')
    for top_list in lists:
        if len(re.findall('list', tree.getpath(top_list))) == 1:
            sublist = top_list.xpath('.//list')
            if sublist:
                print filename, tree.getpath(top_list)
            
