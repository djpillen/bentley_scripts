from lxml import etree
import os
from os.path import join
import re

path = 'C:/Users/Public/Documents/Real_Masters_all'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    for id in tree.xpath("//unitid"):
        if id.text is None:
            idpath = tree.getpath(id)
            print filename
            fout = open('C:/Users/Public/Documents/missingunitid.txt', 'a')
            fout.write(filename + idpath + '\n')
            fout.close()
    print filename
