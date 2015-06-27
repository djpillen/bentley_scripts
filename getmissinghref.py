from lxml import etree
import os
from os.path import join

path = 'C:/Users/Public/Documents/daos'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    for dao in tree.xpath(".//dao"):
        if not dao.get('href'):
            print filename
            fout = open('C:/Users/Public/Documents/missinghref.txt', 'a')
            fout.write(filename + '\n')
            fout.close()
