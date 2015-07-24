from lxml import etree
import os
from os.path import join


path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
outpath = 'C:/Users/djpillen/GitHub/test_dir'

for filename in os.listdir(path):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(join(path,filename), parser)
    unitdates = tree.xpath('//unitdate')
    for u in unitdates:
        if u.tail:
            if u.tail.startswith(' (?)'):
                print filename, u.tail
                u.attrib['certainty'] = "approximate"
    fout = open(join(path,filename), 'w')
    fout.write(etree.tostring(tree,pretty_print=True,xml_declaration=True,encoding='utf-8'))
