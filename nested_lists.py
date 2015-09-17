from lxml import etree
import os
from os.path import join
import re

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    lists = tree.xpath('//list')
    for top_list in lists:
        if not re.findall('list[^$]', tree.getpath(top_list)):
            sublist = top_list.xpath('.//list')
            sublist_found = 0
            while sublist_found == 0:
                if sublist:
                    print filename, tree.getpath(top_list)
                    with open('C:/Users/Public/Documents/to_investigate/nested_lists.txt','a') as outfile:
                        outfile.write(filename + ' ' + tree.getpath(top_list) + '\n')
                    sublist_found += 1
                else:
                    sublist_found += 1
